.PHONY: all build clean

all: build

build:
	cd src && gcc iomt_device_simulator.c -o iomt_device_simulator

clean:
	rm -f src/iomt_device_simulator
