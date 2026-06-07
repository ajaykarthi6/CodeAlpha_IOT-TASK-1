# IoMT Quick Reference

A one-page cheat sheet for common tasks and concepts.

## Quick Commands

### Compile & Run Simulator
```bash
make                  # Compile
./src/iomt_device_simulator --help        # Show options
./src/iomt_device_simulator               # Run default
./src/iomt_device_simulator --format=json --count=5 --device-id=p001
```

### Run Analytics
```bash
python3 analytics/iomt_analytics.py
```

## Normal Vital Sign Ranges (Adult)

| Vital Sign | Normal | Alert |
|------------|--------|-------|
| Heart Rate | 60-100 bpm | <60 or >100 |
| Temperature | 36.5-37.5°C | <36.5 or >37.5 |
| Respiratory Rate | 12-20/min | <12 or >20 |
| Blood Oxygen | 95-100% | <95% |
| Systolic BP | 90-120 mmHg | <90 or >120 |

## FHIR Concept Mapping

| IoMT Concept | FHIR Resource | FHIR Code System |
|--------------|--------------|-----------------|
| Sensor Reading | Observation | LOINC |
| Device | Device | SNOMED CT |
| Patient | Patient | National ID |
| Clinical Note | DocumentReference | SNOMED CT |
| Alert | Task | SNOMED CT |

## Common LOINC Codes

```
8867-4    = Heart Rate
8310-5    = Body Temperature
9279-1    = Respiratory Rate
2708-6    = Blood Oxygen
8480-6    = Systolic Blood Pressure
2345-7    = Glucose Level
```

## Architecture Layers

```
┌─ Application Layer (Dashboards, EHR)
├─ Network Layer (MQTT, HTTPS, VPN)
├─ Edge Layer (Analytics, Alerts)
└─ Device Layer (Sensors, Wearables)
```

## Data Flow

```
Device → Edge Processing → Network → Cloud Storage → Application
         (Anomaly Check)  (Encrypt)  (Time-Series)  (Display)
```

## Anomaly Detection Techniques

| Method | Purpose | Threshold |
|--------|---------|-----------|
| Threshold Check | Clinical ranges | Fixed |
| Z-Score | Statistical outliers | > 2.5 sigma |
| Rate of Change | Rapid deterioration | > threshold/reading |
| Multi-Factor | Composite risk | ≥ 2 abnormalities |
| Trend Analysis | Historical pattern | Slope + seasonality |

## Python Analytics Quick Start

```python
from iomt_analytics import AnomalyDetector, FHIRConverter, SensorReading

# Create reading
reading = SensorReading('Heart Rate', 85, 'bpm', device_id='dev-001')

# Detect anomaly
detector = AnomalyDetector()
result = detector.detect_anomaly('Heart Rate', 85)
print(result['is_anomaly'])  # False (normal)

# Convert to FHIR
fhir = FHIRConverter.to_fhir_observation(reading, patient_id='p-123')
```

## C Simulator Quick Reference

```c
// Key data structure
typedef struct {
    char name[32];      // "Heart Rate"
    float value;        // 82.5
    char unit[8];       // "bpm"
} SensorReading;

// Generate synthetic data
generate_reading(&reading, name, min, max, unit);

// Print as JSON
print_json_readings(readings, count, device_id);

// Check for alerts
analyze_readings(readings, count);
```

## File Locations

| What | Where |
|-----|-------|
| C Simulator | `src/iomt_device_simulator.c` |
| Python Analytics | `analytics/iomt_analytics.py` |
| Technical Design | `design/TECHNICAL_ARCHITECTURE.md` |
| Learning Path | `docs/LEARNING_PATH.md` |
| Tutorials | `docs/TUTORIALS.md` |
| Features List | `docs/FEATURES.md` |

## Learning Milestones

- ✅ Understand IoMT: Read Report Overview (10 min)
- ✅ Run Code: Build and run simulator (5 min)
- ✅ Learn Architecture: Study Technical Design (30 min)
- ✅ Modify Simulator: Add new sensor (1 hour)
- ✅ Process Data: Use Python analytics (1 hour)
- ✅ Build Project: Implement full system (5+ hours)

## Key Concepts

**IoMT:** Internet of Medical Things — connected medical devices for continuous monitoring

**Edge Computing:** Local data processing to reduce latency and improve privacy

**FHIR:** Fast Healthcare Interoperability Resources — standard for health data exchange

**Anomaly Detection:** Identifying abnormal readings using thresholds and statistics

**Remote Patient Monitoring (RPM):** Care delivery outside clinical settings

**HIPAA:** Health Insurance Portability and Accountability Act — U.S. privacy regulation

## Security Checklist

- [ ] Encrypt data at rest
- [ ] Encrypt data in transit (TLS 1.3)
- [ ] Implement authentication
- [ ] Use authorization (RBAC/ABAC)
- [ ] Audit all access
- [ ] Handle PII carefully
- [ ] Test regularly
- [ ] Document policies

## Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Too many alerts | Adjust thresholds or add hysteresis |
| Missed critical events | Lower thresholds, add trend analysis |
| Battery drains fast | Reduce sampling, add adaptive intervals |
| Data silos | Implement FHIR standards |
| Privacy concerns | Encrypt, anonymize, limit access |

## Resources by Role

**Students:** Start → LEARNING_PATH.md → TUTORIALS.md  
**Developers:** Start → src/README.md → TECHNICAL_ARCHITECTURE.md  
**Healthcare:** Start → REPORT_OVERVIEW.md → APPLICATIONS.md  
**Security:** Start → TECHNICAL_ARCHITECTURE.md (Security section)

## Standards Reference

- **FHIR:** HL7 FHIR (hl7.org/fhir)
- **HL7:** Health Level 7 messaging
- **SNOMED CT:** Clinical terminology
- **LOINC:** Lab test naming
- **DICOM:** Medical imaging
- **ICS:** Calendar format
- **HIPAA:** U.S. privacy law
- **GDPR:** EU privacy law
- **IEC 60601:** Medical device safety

## More Information

Full guides:
- [NAVIGATION.md](NAVIGATION.md) — Complete guide to all resources
- [README.md](README.md) — Main project guide
- [LEARNING_PATH.md](docs/LEARNING_PATH.md) — Structured curriculum

---

**Print this page for quick reference while coding! 📋**
