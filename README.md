# CodeAlpha IoMT Research Repository

This repository captures the key findings of the attached IoMT research report and adds an innovative, structured implementation layer for the Internet of Medical Things.

## What is included
- `IoMT_Research_Report.pdf` – the original research report on IoMT healthcare monitoring.
- `docs/` – organized, readable summaries of the report topics:
  - `report_overview.md`
  - `report_applications.md`
  - `report_benefits_challenges.md`
  - `report_references.md`
- `src/` – sample C code that simulates an IoMT wearable device generating healthcare readings.
- `.gitignore` – ignores compiled binaries and temporary build files.

## Repository structure
- `README.md` – this guide.
- `docs/` – detailed explanation of report content and real-world IoMT design concepts.
- `src/` – sample IoMT simulator code in C.
- `IoMT_Research_Report.pdf` – source report.

## Summary of the report
The report demonstrates how IoMT is revolutionizing healthcare by:
- enabling continuous patient monitoring
- improving early detection of health events
- supporting remote patient care and hospital-at-home solutions
- reducing costs while improving patient experience

## Sample IoMT C simulation
The included C simulation demonstrates a simple wearable IoMT device producing:
- heart rate
- body temperature
- glucose level
- blood oxygen
- blood pressure

The program prints JSON-formatted sensor data and watches for abnormal values, mimicking edge-based medical monitoring.

## How to run the sample
1. Open a terminal in the repository root.
2. Compile the simulator:

```bash
cd src
gcc iomt_device_simulator.c -o iomt_device_simulator
```

3. Run the simulator:

```bash
./iomt_device_simulator
```

## Why this repository is unique
This repository is organized to be both research-oriented and practical:
- clear, readable documentation derived from the report
- a concrete C-based prototype for sensor simulation
- a modern structure that separates report insights from implementation

## Next steps
To expand this project, you can add:
- a network client to send data to a cloud endpoint
- a data storage module for time-series analytics
- a companion dashboard for monitoring patient signals in real time

## License
This repository is provided for educational and demonstration purposes.
