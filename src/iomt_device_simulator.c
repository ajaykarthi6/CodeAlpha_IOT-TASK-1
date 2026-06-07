#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "iomt_data_model.h"

void generate_reading(SensorReading *reading, const char *name, float min, float max, const char *unit) {
    strncpy(reading->name, name, SENSOR_NAME_MAX - 1);
    reading->name[SENSOR_NAME_MAX - 1] = '\0';
    reading->value = min + ((float)rand() / RAND_MAX) * (max - min);
    strncpy(reading->unit, unit, SENSOR_UNIT_MAX - 1);
    reading->unit[SENSOR_UNIT_MAX - 1] = '\0';
}

void print_json_readings(const SensorReading readings[], int count, const char *device_id) {
    printf("{\n  \"device\": \"IoMT Wearable Simulator\",\n  \"device_id\": \"%s\",\n  \"timestamp\": %ld,\n  \"readings\": [\n",
           device_id,
           time(NULL));
    for (int i = 0; i < count; i++) {
        printf("    {\"sensor\": \"%s\", \"value\": %.2f, \"unit\": \"%s\"}%s\n",
               readings[i].name,
               readings[i].value,
               readings[i].unit,
               i < count - 1 ? "," : "");
    }
    printf("  ]\n}\n");
}

void print_text_readings(const SensorReading readings[], int count, const char *device_id) {
    printf("IoMT Wearable Simulator (%s) - %ld\n", device_id, time(NULL));
    for (int i = 0; i < count; i++) {
        printf("- %s: %.2f %s\n", readings[i].name, readings[i].value, readings[i].unit);
    }
}

void analyze_readings(const SensorReading readings[], int count) {
    for (int i = 0; i < count; i++) {
        const SensorReading *reading = &readings[i];
        if (strcmp(reading->name, "Heart Rate") == 0) {
            if (reading->value < 60 || reading->value > 100) {
                printf("ALERT: Heart Rate outside normal range: %.2f %s\n", reading->value, reading->unit);
            }
        } else if (strcmp(reading->name, "Body Temperature") == 0) {
            if (reading->value < 36.0f || reading->value > 37.5f) {
                printf("ALERT: Body Temperature outside normal range: %.2f %s\n", reading->value, reading->unit);
            }
        } else if (strcmp(reading->name, "Glucose Level") == 0) {
            if (reading->value < 70 || reading->value > 140) {
                printf("ALERT: Glucose Level outside normal range: %.2f %s\n", reading->value, reading->unit);
            }
        }
    }
}

static void print_usage(const char *program_name) {
    printf("Usage: %s [--count N] [--format json|text] [--device-id ID]\n", program_name);
    printf("  --count N      Generate N sample cycles (default 1)\n");
    printf("  --format MODE  Output mode: json or text (default json)\n");
    printf("  --device-id ID Device identifier for telemetry payloads\n");
}

int main(int argc, char *argv[]) {
    srand((unsigned int)time(NULL));

    int count = 1;
    char format[8] = "json";
    char device_id[32] = "alpha-001";

    for (int i = 1; i < argc; i++) {
        if (strncmp(argv[i], "--count=", 8) == 0) {
            count = atoi(argv[i] + 8);
            if (count < 1) count = 1;
        } else if (strcmp(argv[i], "--count") == 0 && i + 1 < argc) {
            count = atoi(argv[++i]);
            if (count < 1) count = 1;
        } else if (strncmp(argv[i], "--format=", 9) == 0) {
            strncpy(format, argv[i] + 9, sizeof(format) - 1);
            format[sizeof(format) - 1] = '\0';
        } else if (strcmp(argv[i], "--format") == 0 && i + 1 < argc) {
            strncpy(format, argv[++i], sizeof(format) - 1);
            format[sizeof(format) - 1] = '\0';
        } else if (strncmp(argv[i], "--device-id=", 12) == 0) {
            strncpy(device_id, argv[i] + 12, sizeof(device_id) - 1);
            device_id[sizeof(device_id) - 1] = '\0';
        } else if (strcmp(argv[i], "--device-id") == 0 && i + 1 < argc) {
            strncpy(device_id, argv[++i], sizeof(device_id) - 1);
            device_id[sizeof(device_id) - 1] = '\0';
        } else if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            return 0;
        } else {
            print_usage(argv[0]);
            return 1;
        }
    }

    SensorReading readings[5];

    for (int cycle = 0; cycle < count; cycle++) {
        generate_reading(&readings[0], "Heart Rate", 55.0f, 110.0f, "bpm");
        generate_reading(&readings[1], "Body Temperature", 35.8f, 38.0f, "C");
        generate_reading(&readings[2], "Glucose Level", 65.0f, 170.0f, "mg/dL");
        generate_reading(&readings[3], "Blood Oxygen", 89.0f, 100.0f, "%");
        generate_reading(&readings[4], "Blood Pressure Systolic", 100.0f, 145.0f, "mmHg");

        if (strcmp(format, "text") == 0) {
            print_text_readings(readings, 5, device_id);
        } else {
            print_json_readings(readings, 5, device_id);
        }

        analyze_readings(readings, 5);

        if (cycle + 1 < count) {
            printf("\n");
        }
    }

    return 0;
}
