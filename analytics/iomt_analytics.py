#!/usr/bin/env python3
"""
IoMT Analytics Module

Provides educational examples of data processing, trend detection,
and FHIR format conversion for IoMT sensor data.
"""

import json
import statistics
from datetime import datetime
from typing import List, Dict, Any


class SensorReading:
    """Represents a single sensor measurement."""
    
    def __init__(self, sensor: str, value: float, unit: str, 
                 device_id: str = "device-001", timestamp: int = None):
        self.sensor = sensor
        self.value = value
        self.unit = unit
        self.device_id = device_id
        self.timestamp = timestamp or int(datetime.now().timestamp())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sensor': self.sensor,
            'value': self.value,
            'unit': self.unit,
            'device_id': self.device_id,
            'timestamp': self.timestamp
        }


class AnomalyDetector:
    """Detects anomalies in sensor readings."""
    
    # Clinical normal ranges
    NORMAL_RANGES = {
        'Heart Rate': (60, 100),
        'Body Temperature': (36.5, 37.5),
        'Glucose Level': (70, 140),
        'Blood Oxygen': (95, 100),
        'Blood Pressure Systolic': (90, 120),
        'Respiratory Rate': (12, 20),
    }
    
    def __init__(self, buffer_size: int = 10):
        """Initialize anomaly detector with circular buffer."""
        self.buffer_size = buffer_size
        self.readings_buffer = {}
    
    def add_reading(self, sensor_name: str, value: float) -> None:
        """Add a reading to the buffer."""
        if sensor_name not in self.readings_buffer:
            self.readings_buffer[sensor_name] = []
        
        self.readings_buffer[sensor_name].append(value)
        
        # Keep buffer size limited
        if len(self.readings_buffer[sensor_name]) > self.buffer_size:
            self.readings_buffer[sensor_name].pop(0)
    
    def is_threshold_violation(self, sensor_name: str, value: float) -> bool:
        """Check if reading violates normal range."""
        if sensor_name not in self.NORMAL_RANGES:
            return False
        
        low, high = self.NORMAL_RANGES[sensor_name]
        return value < low or value > high
    
    def compute_zscore(self, sensor_name: str, value: float) -> float:
        """Compute Z-score for anomaly detection."""
        if sensor_name not in self.readings_buffer:
            return 0.0
        
        readings = self.readings_buffer[sensor_name]
        if len(readings) < 2:
            return 0.0
        
        mean = statistics.mean(readings)
        stdev = statistics.stdev(readings)
        
        if stdev == 0:
            return 0.0
        
        return abs((value - mean) / stdev)
    
    def detect_anomaly(self, sensor_name: str, value: float) -> Dict[str, Any]:
        """Comprehensive anomaly detection."""
        self.add_reading(sensor_name, value)
        
        threshold_violation = self.is_threshold_violation(sensor_name, value)
        zscore = self.compute_zscore(sensor_name, value)
        
        anomaly_score = 0
        reasons = []
        
        if threshold_violation:
            anomaly_score += 50
            reasons.append("Threshold violation")
        
        if zscore > 2.5:  # 99% confidence
            anomaly_score += 30
            reasons.append(f"Extreme Z-score: {zscore:.2f}")
        elif zscore > 2.0:  # 95% confidence
            anomaly_score += 15
            reasons.append(f"High Z-score: {zscore:.2f}")
        
        return {
            'is_anomaly': anomaly_score > 50,
            'anomaly_score': min(100, anomaly_score),
            'zscore': zscore,
            'reasons': reasons
        }


class FHIRConverter:
    """Converts IoMT sensor data to FHIR format."""
    
    # LOINC code mappings
    LOINC_CODES = {
        'Heart Rate': '8867-4',
        'Body Temperature': '8310-5',
        'Respiratory Rate': '9279-1',
        'Blood Oxygen': '2708-6',
        'Blood Pressure Systolic': '8480-6',
        'Glucose Level': '2345-7',
    }
    
    @staticmethod
    def to_fhir_observation(reading: SensorReading, 
                           patient_id: str = "patient-001") -> Dict[str, Any]:
        """Convert sensor reading to FHIR Observation resource."""
        
        loinc_code = FHIRConverter.LOINC_CODES.get(reading.sensor, "unknown")
        
        fhir_obs = {
            "resourceType": "Observation",
            "id": f"obs-{reading.sensor.lower().replace(' ', '-')}-{reading.timestamp}",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": loinc_code,
                        "display": reading.sensor
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "performer": [
                {
                    "reference": f"Device/{reading.device_id}"
                }
            ],
            "effectiveDateTime": datetime.fromtimestamp(
                reading.timestamp).isoformat() + "Z",
            "valueQuantity": {
                "value": reading.value,
                "unit": reading.unit,
                "system": "http://unitsofmeasure.org",
                "code": FHIRConverter._ucum_code(reading.unit)
            }
        }
        
        return fhir_obs
    
    @staticmethod
    def _ucum_code(unit: str) -> str:
        """Map units to UCUM codes."""
        mapping = {
            'bpm': '{beats}/min',
            'C': 'Cel',
            'F': '[degF]',
            '%': '%',
            'mg/dL': 'mg/dL',
            'mmHg': 'mm[Hg]',
        }
        return mapping.get(unit, unit)


class TrendAnalyzer:
    """Analyzes trends in sensor data over time."""
    
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.values = []
    
    def add_value(self, value: float) -> None:
        """Add a value to the trend analysis window."""
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.values.pop(0)
    
    def get_trend(self) -> str:
        """Determine trend direction: rising, falling, or stable."""
        if len(self.values) < 2:
            return "insufficient_data"
        
        # Simple linear regression
        n = len(self.values)
        mean_x = (n - 1) / 2
        mean_y = statistics.mean(self.values)
        
        numerator = sum((i - mean_x) * (self.values[i] - mean_y) 
                       for i in range(n))
        denominator = sum((i - mean_x) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        if slope > 0.5:
            return "rising"
        elif slope < -0.5:
            return "falling"
        else:
            return "stable"
    
    def get_rate_of_change(self) -> float:
        """Calculate rate of change per reading."""
        if len(self.values) < 2:
            return 0.0
        
        return self.values[-1] - self.values[-2]
    
    def get_statistics(self) -> Dict[str, float]:
        """Get statistical summary."""
        if not self.values:
            return {}
        
        return {
            'mean': statistics.mean(self.values),
            'median': statistics.median(self.values),
            'stdev': statistics.stdev(self.values) if len(self.values) > 1 else 0,
            'min': min(self.values),
            'max': max(self.values),
            'current': self.values[-1]
        }


# Example usage and educational demonstrations
if __name__ == "__main__":
    print("=" * 60)
    print("IoMT Analytics Module - Educational Examples")
    print("=" * 60)
    
    # Example 1: Anomaly Detection
    print("\n[Example 1: Anomaly Detection]")
    detector = AnomalyDetector()
    
    readings = [
        ('Heart Rate', 75),
        ('Heart Rate', 78),
        ('Heart Rate', 76),
        ('Heart Rate', 150),  # Abnormal!
    ]
    
    for sensor, value in readings:
        result = detector.detect_anomaly(sensor, value)
        status = "ANOMALY" if result['is_anomaly'] else "NORMAL"
        print(f"{sensor}: {value} → {status} (score: {result['anomaly_score']})")
    
    # Example 2: FHIR Conversion
    print("\n[Example 2: FHIR Format Conversion]")
    reading = SensorReading(
        sensor='Heart Rate',
        value=82.5,
        unit='bpm',
        device_id='wearable-001'
    )
    
    fhir_obs = FHIRConverter.to_fhir_observation(reading, 'patient-123')
    print(json.dumps(fhir_obs, indent=2))
    
    # Example 3: Trend Analysis
    print("\n[Example 3: Trend Analysis]")
    analyzer = TrendAnalyzer(window_size=5)
    
    heart_rate_trend = [70, 72, 75, 78, 82, 85, 88]
    for hr in heart_rate_trend:
        analyzer.add_value(hr)
        stats = analyzer.get_statistics()
        trend = analyzer.get_trend()
        roc = analyzer.get_rate_of_change()
        
        print(f"HR: {hr} bpm | Trend: {trend} | "
              f"Rate of Change: {roc:.1f} bpm | "
              f"Mean: {stats['mean']:.1f} bpm")
    
    # Example 4: Multi-Reading Analysis
    print("\n[Example 4: Multi-Reading Patient Assessment]")
    readings_data = [
        SensorReading('Heart Rate', 95, 'bpm'),
        SensorReading('Body Temperature', 37.8, 'C'),
        SensorReading('Blood Oxygen', 92, '%'),
    ]
    
    detector_multi = AnomalyDetector()
    anomaly_count = 0
    
    for reading in readings_data:
        result = detector_multi.detect_anomaly(reading.sensor, reading.value)
        if result['is_anomaly']:
            anomaly_count += 1
            print(f"⚠️  {reading.sensor}: {reading.value} {reading.unit} - {result['reasons']}")
        else:
            print(f"✓ {reading.sensor}: {reading.value} {reading.unit} - Normal")
    
    if anomaly_count >= 2:
        print("\n🚨 CRITICAL: Multiple vital signs abnormal - recommend immediate clinician review")
    
    print("\n" + "=" * 60)
