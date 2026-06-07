# Technical Architecture

## System Overview

The CodeAlpha IoMT system is architected as a layered, modular platform designed for real-world healthcare deployment. The architecture separates concerns across device, edge, network, and application layers.

```
┌─────────────────────────────────────────────────────────────┐
│            APPLICATION LAYER                                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │ Clinician       │  │ Patient Mobile   │  │ Analytics │ │
│  │ Dashboard       │  │ Application      │  │ Platform  │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
└────────────────┬────────────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │ FHIR / HL7     │
         │ Secure REST    │
         └───────┬────────┘
                 │
┌─────────────────────────────────────────────────────────────┐
│            NETWORK LAYER                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MQTT / Secure WebSocket / VPN Tunnel               │  │
│  │  End-to-End Encryption (AES-256)                   │  │
│  │  TLS 1.3 Certificate-based Authentication          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────────────┐
│            EDGE/GATEWAY LAYER                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Local Analytics & Decision Engine                   │  │
│  │ ┌──────────────────┐  ┌──────────────────────────┐  │  │
│  │ │ Real-time Event  │  │ Anomaly Detection &     │  │  │
│  │ │ Processor        │  │ Local Alert Generation  │  │  │
│  │ └──────────────────┘  └──────────────────────────┘  │  │
│  │ ┌──────────────────┐  ┌──────────────────────────┐  │  │
│  │ │ Temporary Buffer │  │ Data Encryption &       │  │  │
│  │ │ & Sync Queue     │  │ Privacy Compliance      │  │  │
│  │ └──────────────────┘  └──────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────────────────┐
│            DEVICE LAYER                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Wearable Biosensors / Smart Implants / Ambient     │  │
│  │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌───────────┐ │  │
│  │ │ ECG  │ │ Temp │ │ Gluc │ │ O2   │ │ Pressure  │ │  │
│  │ │Patch │ │Sensor│ │ Monitor    │ │ Monitor   │ │  │
│  │ └──────┘ └──────┘ └──────┘ └──────┘ └───────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Device Layer

**Responsibility:** Sensor data acquisition and basic local processing

**Components:**
- **Wearable Sensors:** Continuous biosignal monitoring
- **Ingestible Sensors:** Smart pills with medication adherence tracking
- **Smart Implants:** Connected pacemakers, insulin pumps, glucose monitors
- **Ambient Monitors:** Environmental sensors for contextual health data

**Data Model:**
```c
typedef struct {
    char name[32];          // e.g., "Heart Rate"
    float value;            // Measured value
    char unit[8];           // e.g., "bpm"
    time_t timestamp;       // When measurement was taken
    char device_id[32];     // Source device identifier
} SensorReading;
```

### 2. Edge Layer

**Responsibility:** Local analytics, anomaly detection, and intelligent buffering

**Key Features:**
- **Real-time Processing:** No cloud latency for critical decisions
- **Anomaly Detection:** Statistical thresholds and ML-based detection
- **Local Alerting:** Immediate notification to patient and caregivers
- **Data Buffering:** Temporary storage with sync queue management
- **Security:** Encryption and key management at edge

**Processing Pipeline:**
```
Raw Sensor Data
      ↓
[Validation & Normalization]
      ↓
[Feature Extraction]
      ↓
[Anomaly Scoring]
      ↓
[Threshold Evaluation]
      ↓
[Alert Generation or Silent Logging]
      ↓
[Network Transmission / Local Storage]
```

### 3. Network Layer

**Responsibility:** Secure, reliable data transmission

**Protocols:**
- **MQTT:** Lightweight publish-subscribe for IoT
- **HTTPS/REST:** For clinical integration endpoints
- **WebSocket:** Real-time bidirectional communication
- **VPN/WireGuard:** Secure tunnel for enterprise deployments

**Security Features:**
- TLS 1.3 encryption
- Certificate-based mutual authentication
- Message signing and verification
- Replay attack prevention

### 4. Application Layer

**Responsibility:** Clinical workflows, visualization, and analytics

**Modules:**
- **Clinician Dashboard:** Real-time patient monitoring and historical analysis
- **Patient Mobile App:** Personal health tracking and medication reminders
- **Analytics Platform:** Population health, predictive modeling, research
- **Integration Hub:** FHIR/HL7/DICOM connectors to hospital systems

## Data Flow Architecture

### Normal Operation Flow
```
Device → Raw Sensor Data
         ↓
    Edge Processing
    ├─ Validate data
    ├─ Compute anomaly score
    ├─ Check thresholds
    └─ Encrypt payload
         ↓
    Network Transmission
    ├─ MQTT publish or REST POST
    ├─ Local buffering if offline
    └─ Retry logic
         ↓
    Cloud Ingestion
    ├─ Data verification
    ├─ Time-series storage
    └─ Trigger workflows
         ↓
    Application Services
    ├─ Update dashboards
    ├─ Store in EHR
    └─ Generate insights
```

### Critical Alert Flow
```
Anomaly Detected
    ↓
[Local Decision]
    ├─ Is this critical?
    └─ YES → Immediate Action
         ↓
    Alert Notification
    ├─ Patient vibration/tone
    ├─ Caregiver SMS
    ├─ Clinician push notification
    └─ Hospital system integration
```

## Security Architecture

### Multi-Layer Defense Strategy

**Device Level:**
- Secure enclave for key storage
- Tamper detection
- Hardware-backed encryption

**Edge Level:**
- Zero-trust network architecture
- Local rate limiting
- Intrusion detection

**Network Level:**
- TLS 1.3 with AEAD cipher suites
- Certificate pinning
- DDoS mitigation

**Application Level:**
- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)
- Audit logging and compliance reporting

## Scalability Considerations

### Horizontal Scaling
```
Multiple Device Streams
     ↓
[Load Balancer]
     ↓
Message Queue (Kafka/RabbitMQ)
     ↓
Stream Processing Cluster
     ↓
Time-Series Database (InfluxDB)
```

### Vertical Scaling
- Edge device optimization for resource-constrained environments
- Efficient C implementation for minimal memory footprint
- Asynchronous I/O for concurrent device handling

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Sensor Latency | < 1ms | End-to-end from sensor read to decision |
| Alert Latency | < 100ms | From anomaly to notification |
| Network Throughput | > 1Mbps | Per device aggregate |
| Cloud Processing | < 500ms | From ingestion to storage |
| Dashboard Refresh | < 2s | Real-time visualization |
| System Uptime | 99.99% | High availability requirement |

## Deployment Topologies

### 1. Clinic/Hospital Deployment
- On-premises edge gateway
- Private network isolation
- EHR system integration
- IT-managed security

### 2. Home Care Deployment
- WiFi/Cellular gateway
- Cloud-based backend
- Patient self-management
- Encrypted cloud storage

### 3. Hybrid Deployment
- Mix of on-premises and cloud
- Data residency compliance
- Flexible architecture
- Cost optimization

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Device Firmware | C | Minimal overhead, broad compatibility |
| Edge Processing | C/Embedded Linux | Real-time requirements, power efficiency |
| Network Protocol | MQTT | Lightweight, reliable, pub-sub pattern |
| Cloud Backend | Python/Node.js | Developer productivity, data processing |
| Time-Series DB | InfluxDB/TimescaleDB | Optimized for medical telemetry |
| API Gateway | Kong/AWS API Gateway | Security, rate limiting, auth |
| Message Queue | Kafka/RabbitMQ | Reliable event streaming |
| Monitoring | Prometheus/Grafana | Infrastructure and application metrics |

## Interoperability Standards

- **FHIR (Fast Healthcare Interoperability Resources):** RESTful healthcare data exchange
- **HL7 v2/v3:** Legacy EHR system integration
- **DICOM:** Medical imaging and device communication
- **ICS (iCalendar):** Appointment and reminder scheduling
- **LOINC:** Standardized medical test naming
- **SNOMED CT:** Clinical terminology mapping
