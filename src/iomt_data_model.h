#ifndef IOMT_DATA_MODEL_H
#define IOMT_DATA_MODEL_H

#define SENSOR_NAME_MAX 32
#define SENSOR_UNIT_MAX 8

typedef struct {
    char name[SENSOR_NAME_MAX];
    float value;
    char unit[SENSOR_UNIT_MAX];
} SensorReading;

void generate_reading(SensorReading *reading, const char *name, float min, float max, const char *unit);
void print_json_readings(const SensorReading readings[], int count);
void analyze_readings(const SensorReading readings[], int count);

#endif // IOMT_DATA_MODEL_H
