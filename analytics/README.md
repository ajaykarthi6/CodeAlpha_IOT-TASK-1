# Analytics Module Guide

This folder contains educational Python code for IoMT data analysis and processing.

## Files

- `iomt_analytics.py` — Analytics library with anomaly detection, FHIR conversion, and trend analysis

## Quick Start

Run the educational examples:

```bash
python3 iomt_analytics.py
```

## Main Classes

### SensorReading
Represents a single measurement from an IoMT device.

```python
from iomt_analytics import SensorReading

reading = SensorReading(
    sensor='Heart Rate',
    value=82.5,
    unit='bpm',
    device_id='wearable-001'
)
```

### AnomalyDetector
Detects abnormal readings using statistical methods and clinical thresholds.

```python
from iomt_analytics import AnomalyDetector

detector = AnomalyDetector()
result = detector.detect_anomaly('Heart Rate', 150)
print(result)  # {'is_anomaly': True, 'anomaly_score': 80, ...}
```

### FHIRConverter
Converts IoMT data to standard healthcare format.

```python
from iomt_analytics import FHIRConverter

fhir_obs = FHIRConverter.to_fhir_observation(reading, patient_id='patient-123')
print(fhir_obs)  # FHIR-compliant JSON
```

### TrendAnalyzer
Analyzes temporal patterns in sensor data.

```python
from iomt_analytics import TrendAnalyzer

analyzer = TrendAnalyzer(window_size=5)
for value in [70, 72, 75, 78, 82]:
    analyzer.add_value(value)
    print(analyzer.get_trend())  # 'rising', 'falling', or 'stable'
```

## Educational Use Cases

1. **Understand Anomaly Detection:**
   - How Z-scores identify statistical outliers
   - Why clinical thresholds matter
   - Multi-factor alert strategies

2. **Learn FHIR Standard:**
   - Mapping medical concepts to standardized codes
   - Generating FHIR observations
   - Preparing for EHR integration

3. **Explore Time-Series Analysis:**
   - Trend detection in vital signs
   - Moving average calculations
   - Rate of change detection

## Integration with C Simulator

Convert C simulator output to analytics:

```bash
# Generate JSON from C simulator
./src/iomt_device_simulator --format=json > /tmp/readings.json

# Process with Python analytics
python3 analytics/process_readings.py /tmp/readings.json
```

## Further Reading

- [Learning Path](../docs/LEARNING_PATH.md) — structured educational journey
- [Tutorials](../docs/TUTORIALS.md) — hands-on exercises
- [Technical Architecture](../design/TECHNICAL_ARCHITECTURE.md) — system design details
