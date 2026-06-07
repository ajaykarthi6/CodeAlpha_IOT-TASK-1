# Educational Tutorials

## Tutorial 1: Understanding Vital Sign Thresholds

### Objective
Learn why normal vital sign ranges matter in IoMT and how to set appropriate clinical thresholds.

### Background
IoMT devices rely on accurate, clinically-validated thresholds to distinguish normal from abnormal states. Setting thresholds incorrectly leads to either missed critical events or alarm fatigue.

### Normal Vital Signs (Adult)

| Vital Sign | Normal Range | Clinical Concern |
|------------|--------------|------------------|
| Heart Rate | 60-100 bpm | Bradycardia (<60) or Tachycardia (>100) |
| Respiratory Rate | 12-20 breaths/min | Tachypnea (>20) or Bradypnea (<12) |
| Body Temperature | 36.5-37.5°C | Hypothermia or Fever |
| Blood Oxygen (SpO2) | 95-100% | Hypoxemia (<95%) |
| Systolic BP | 90-120 mmHg | Hypotension or Hypertension |
| Diastolic BP | 60-80 mmHg | - |

### Why Ranges Vary

1. **Age Factor:** Elderly may have different normal ranges
2. **Fitness Level:** Athletes may have lower resting heart rate
3. **Medications:** Beta-blockers can lower heart rate
4. **Activity State:** Exercise increases HR and respiratory rate
5. **Individual Baseline:** Each patient has their own normal

### Hands-on: Modify Threshold Logic

**Current Implementation (static thresholds):**
```c
if (reading->value < 60 || reading->value > 100) {
    printf("ALERT: Heart Rate outside normal range\n");
}
```

**Better Approach (context-aware):**
```c
// Patient-specific thresholds based on profile
float hr_low = (patient.is_athlete) ? 45.0 : 60.0;
float hr_high = (patient.is_elderly) ? 90.0 : 100.0;

if (reading->value < hr_low || reading->value > hr_high) {
    printf("ALERT: Heart Rate abnormal for this patient\n");
}
```

**Exercise:** Modify the simulator to accept patient profile flags and adjust thresholds accordingly.

---

## Tutorial 2: From Simulator Output to FHIR Format

### Objective
Learn to convert IoMT sensor data into standard healthcare data format.

### Current Simulator Output
```json
{
  "device": "IoMT Wearable Simulator",
  "device_id": "alpha-001",
  "timestamp": 1720000000,
  "readings": [
    {"sensor": "Heart Rate", "value": 82.24, "unit": "bpm"}
  ]
}
```

### Target FHIR Format
```json
{
  "resourceType": "Observation",
  "id": "obs-hr-001",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "8867-4",
        "display": "Heart rate"
      }
    ]
  },
  "subject": {
    "reference": "Patient/patient-001"
  },
  "performer": [
    {
      "reference": "Device/device-alpha-001"
    }
  ],
  "effectiveDateTime": "2026-06-07T10:30:00Z",
  "valueQuantity": {
    "value": 82.24,
    "unit": "bpm",
    "system": "http://unitsofmeasure.org",
    "code": "{beats}/min"
  },
  "interpretation": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
          "code": "N",
          "display": "Normal"
        }
      ]
    }
  ]
}
```

### Mapping Table

| Simulator Field | FHIR Field | Transformation |
|----------------|-----------|-----------------|
| sensor | code | Map to LOINC code |
| value | valueQuantity.value | Direct copy |
| unit | valueQuantity.unit | Map to UCUM standard |
| device_id | performer | Reference to device |
| timestamp | effectiveDateTime | Convert to ISO 8601 |

### LOINC Code Mappings

Common vital signs to LOINC codes:
- Heart Rate: 8867-4
- Body Temperature: 8310-5
- Respiratory Rate: 9279-1
- Blood Oxygen: 2708-6
- Systolic Blood Pressure: 8480-6
- Diastolic Blood Pressure: 8462-4

### Exercise: Build a Converter

Write a Python function to convert simulator JSON to FHIR:

```python
def sensor_to_fhir(sensor_reading, patient_id, device_id):
    """Convert sensor reading to FHIR Observation"""
    
    # Map sensor names to LOINC codes
    loinc_map = {
        "Heart Rate": "8867-4",
        "Body Temperature": "8310-5",
        # ... etc
    }
    
    fhir_obs = {
        "resourceType": "Observation",
        "id": f"obs-{sensor_reading['sensor']}-{int(time.time())}",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": loinc_map.get(sensor_reading['sensor']),
                    "display": sensor_reading['sensor']
                }
            ]
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "performer": [{"reference": f"Device/{device_id}"}],
        "effectiveDateTime": datetime.fromtimestamp(
            sensor_reading['timestamp']).isoformat() + "Z",
        "valueQuantity": {
            "value": sensor_reading['value'],
            "unit": sensor_reading['unit']
        }
    }
    
    return fhir_obs
```

---

## Tutorial 3: Implementing Edge-Based Anomaly Detection

### Objective
Build a more sophisticated anomaly detection algorithm that considers patient history and context.

### Simple Threshold Approach (Current)
```c
if (reading->value < threshold_low || reading->value > threshold_high) {
    ALERT;
}
```

**Limitations:**
- No historical context
- False positives from transient spikes
- No personalization

### Improved Approaches

#### 1. Moving Average with Deviation
```c
#define BUFFER_SIZE 10

typedef struct {
    float readings[BUFFER_SIZE];
    int index;
    int count;
} ReadingBuffer;

float compute_zscore(ReadingBuffer *buffer, float new_reading) {
    // Calculate mean
    float sum = 0;
    for (int i = 0; i < buffer->count; i++) {
        sum += buffer->readings[i];
    }
    float mean = sum / buffer->count;
    
    // Calculate standard deviation
    float variance = 0;
    for (int i = 0; i < buffer->count; i++) {
        variance += (buffer->readings[i] - mean) * 
                   (buffer->readings[i] - mean);
    }
    float stddev = sqrt(variance / buffer->count);
    
    // Z-score: how many std devs from mean
    float zscore = (new_reading - mean) / stddev;
    return fabs(zscore);
}

// Use case: alert if z-score > 2.5 (99% confidence)
```

#### 2. Rate of Change Detection
```c
bool detect_rapid_change(float current, float previous) {
    float change_rate = fabs(current - previous);
    
    // Alert if heart rate changes by > 10 bpm in one reading
    if (change_rate > 10.0) {
        return true;  // ALERT
    }
    return false;
}
```

#### 3. Temporal Pattern Recognition
```c
// Detect if multiple abnormalities occur together
typedef struct {
    bool high_hr;
    bool high_temp;
    bool low_oxygen;
} AnomalyFlags;

void multi_factor_alert(AnomalyFlags flags) {
    int anomaly_count = 0;
    if (flags.high_hr) anomaly_count++;
    if (flags.high_temp) anomaly_count++;
    if (flags.low_oxygen) anomaly_count++;
    
    // Alert if 2 or more factors indicate problem
    if (anomaly_count >= 2) {
        printf("CRITICAL: Multiple vital signs abnormal\n");
    }
}
```

### Exercise: Implement Adaptive Thresholds

Create a system where normal ranges adapt based on time of day:
- Morning resting HR: lower threshold
- During exercise: higher threshold  
- Sleep: lowest threshold

---

## Tutorial 4: Multi-Device Coordination

### Objective
Understand how multiple IoMT devices on one patient can work together.

### Scenario: Diabetic Patient

**Device 1:** Continuous Glucose Monitor (CGM)
- Glucose level every 5 minutes
- Alerts on high/low glucose

**Device 2:** Smart Watch
- Heart rate monitoring
- Activity tracking

**Device 3:** Connected Insulin Pump
- Delivers insulin
- Tracks doses

### Cross-Device Logic

```c
void coordinate_devices(
    SensorReading glucose,
    SensorReading heart_rate,
    float recent_activity_level) {
    
    // If glucose is high AND heart rate is elevated
    // AND activity is low → likely stress hyperglycemia
    if (glucose.value > 200 && 
        heart_rate.value > 90 && 
        recent_activity_level < 0.3) {
        printf("Stress hyperglycemia detected\n");
        // Recommend behavioral intervention first
        // before insulin adjustment
    }
    
    // If glucose is low AND activity is high
    // → likely exercise-induced hypoglycemia
    if (glucose.value < 70 && recent_activity_level > 0.8) {
        printf("Exercise hypoglycemia risk\n");
        // Recommend carbohydrate intake
    }
}
```

### Exercise: Build a 3-Device Simulator

Extend the simulator to:
1. Track multiple devices simultaneously
2. Correlate readings across devices
3. Generate multi-device alerts
4. Support device-to-device communication

---

## Tutorial 5: Privacy and Security Considerations

### Objective
Understand how to protect sensitive health data in IoMT systems.

### Data Classification

**Highly Sensitive (Require maximum protection):**
- Patient identity
- Genetic information
- Mental health data
- HIV/AIDS status

**Sensitive (Require strong protection):**
- Vital signs and measurements
- Medical history
- Medication lists

**Less Sensitive (Standard protection):**
- Aggregated statistics
- De-identified research data

### Encryption Strategy

```c
// Pseudocode for secure transmission

void send_secure_reading(SensorReading reading, char *patient_id) {
    // 1. Create payload
    char json_payload[512];
    sprintf(json_payload, "{\"sensor\":\"%s\",\"value\":%.2f}", 
            reading.name, reading.value);
    
    // 2. Add timestamp (prevents replay attacks)
    time_t now = time(NULL);
    
    // 3. Encrypt with AES-256
    unsigned char encrypted[1024];
    int encrypted_len = encrypt_aes256(json_payload, encrypted);
    
    // 4. Add digital signature
    unsigned char signature[32];
    hmac_sha256(encrypted, encrypted_len, signature);
    
    // 5. Send encrypted + signature + timestamp
    send_to_server(encrypted, encrypted_len, signature, now);
}
```

### Privacy Best Practices

1. **Data Minimization:** Only collect what's clinically necessary
2. **Purpose Limitation:** Use data only for stated purpose
3. **Storage Limitation:** Delete data when no longer needed
4. **Access Control:** Give clinicians only what they need

### Exercise: Design a Privacy Consent Form

Create a consent form that explains:
- What data will be collected
- How it will be used
- Who has access
- How it will be protected
- Patient's rights and options

---

## Tutorial 6: Building Predictive Alerts

### Objective
Develop a system that predicts health deterioration before critical events.

### Example: Heart Failure Decompensation

**Early Warning Signs:**
1. Weight gain > 2 lbs in 2 days (fluid retention)
2. Increasing shortness of breath
3. Elevated resting heart rate trend
4. Decreased activity level

### Implementation

```c
typedef struct {
    float daily_weights[7];
    float daily_activity[7];
    float daily_avg_hr[7];
    int day_index;
} PatientHistory;

bool predict_decompensation(PatientHistory *history, 
                            float today_weight,
                            float today_activity,
                            float today_hr) {
    // Calculate weight gain trend
    float weight_change = today_weight - history->daily_weights[6];
    
    // Calculate HR trend
    float hr_trend = 0;
    for (int i = 0; i < 7; i++) {
        hr_trend += history->daily_avg_hr[i];
    }
    hr_trend = hr_trend / 7;  // Average
    
    // Calculate activity decline
    float activity_decline = history->daily_activity[6] - today_activity;
    
    // Composite risk score (0-100)
    float risk_score = 0;
    if (weight_change > 2.0) risk_score += 30;
    if (today_hr > hr_trend + 10) risk_score += 25;
    if (activity_decline > 0.2) risk_score += 25;
    
    if (risk_score > 50) {
        printf("HIGH RISK: Possible heart failure decompensation\n");
        printf("Risk Score: %.1f/100\n", risk_score);
        // Recommend increased monitoring or clinic visit
        return true;
    }
    
    return false;
}
```

### Machine Learning Alternative

For more sophisticated prediction, consider ML models:
- Logistic Regression for binary outcomes
- Random Forest for multiple factors
- Neural Networks for complex patterns
- LSTM for time-series analysis

---

## Troubleshooting Guide

### Issue: False Alarms Are Too Frequent

**Solution:**
- Review and adjust clinical thresholds
- Add hysteresis (require threshold violation for multiple readings)
- Increase context awareness (time of day, activity level, etc.)

### Issue: Missing Critical Events

**Solution:**
- Lower alert thresholds cautiously
- Implement multi-factor detection logic
- Add historical trend analysis

### Issue: Device Battery Drains Quickly

**Solution:**
- Reduce sampling frequency if clinically acceptable
- Implement adaptive sampling (higher when anomalies detected)
- Use edge processing to avoid constant cloud transmission

---

## Assessment Checkpoints

After completing these tutorials, you should be able to:

- [ ] Explain why normal vital sign ranges matter
- [ ] Convert IoMT data to FHIR format
- [ ] Implement basic anomaly detection
- [ ] Understand multi-device coordination
- [ ] Apply privacy and security principles
- [ ] Design predictive alert systems
- [ ] Troubleshoot common IoMT issues
