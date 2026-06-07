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

void print_json_readings(const SensorReading readings[], int count) {
    printf("{\n  \"device\": \"IoMT Wearable Simulator\",\n  \"timestamp\": %ld,\n  \"readings\": [\n", time(NULL));
    for (int i = 0; i < count; i++) {
        printf("    {\"sensor\": \"%s\", \"value\": %.2f, \"unit\": \"%s\"}%s\n",
               readings[i].name,
               readings[i].value,
               readings[i].unit,
               i < count - 1 ? "," : "");
    }
    printf("  ]\n}\n");
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

int main(void) {
    srand((unsigned int)time(NULL));

    SensorReading readings[5];
    generate_reading(&readings[0], "Heart Rate", 55.0f, 110.0f, "bpm");
    generate_reading(&readings[1], "Body Temperature", 35.8f, 38.0f, "C");
    generate_reading(&readings[2], "Glucose Level", 65.0f, 170.0f, "mg/dL");
    generate_reading(&readings[3], "Blood Oxygen", 89.0f, 100.0f, "%");
    generate_reading(&readings[4], "Blood Pressure Systolic", 100.0f, 145.0f, "mmHg");

    print_json_readings(readings, 5);
    analyze_readings(readings, 5);

    return 0;
}
