# Source Code Guide

This folder contains the sample IoMT wearable simulator written in C.

## Purpose
The simulator produces synthetic medical sensor readings, prints them in JSON format, and checks for abnormal values. It serves as a practical prototype for edge computing in IoMT.

## Files
- `iomt_data_model.h` — defines the sensor reading data model and helper signatures.
- `iomt_device_simulator.c` — generates simulated vital sign data and performs local anomaly detection.

## Build and run
From the repository root:

```bash
cd src
make
./iomt_device_simulator --format=json --count=1
```

## Supported options
- `--count <n>` — number of sample cycles to generate
- `--format=json|text` — output format for the simulated data
- `--device-id <id>` — attach a device identifier to the payload

## Example output
```json
{
  "device": "IoMT Wearable Simulator",
  "device_id": "alpha-001",
  "timestamp": 1720000000,
  "readings": [ ... ]
}
```

## Extend the simulator
- add a network client to post JSON payloads to a cloud endpoint
- implement battery life and sensor health models
- add a file logger for historic trend analysis
