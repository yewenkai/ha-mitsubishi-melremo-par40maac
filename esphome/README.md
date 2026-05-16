# ESPHome Configuration And Firmware Build

[中文说明](README-zh.md)

This directory contains an example ESP32-S3 Dongle configuration for Home Assistant Bluetooth Proxy.

Before use, copy the secrets template:

```bash
cp secrets.yaml.example secrets.yaml
```

Enter your own WiFi information before compiling or flashing through ESPHome Dashboard.

## Path 1: Official Docker / ESPHome Dashboard

On a Linux host, run ESPHome Dashboard with Docker:

```bash
docker compose -f docker-compose.esphome.linux.yml up -d
```

Then import or edit `esp32-s3-dongle.yaml` in the Dashboard and compile or update over OTA.

For the first flash, connect the ESP32-S3 to a computer or host with USB serial access and follow the ESPHome Dashboard flashing flow.

## Path 2: Local Conda Environment

You can also create an isolated Python environment with conda:

```bash
conda create -n esphome python=3.12 -y
conda activate esphome
pip install esphome
```

Check the configuration:

```bash
esphome config esp32-s3-dongle.yaml
```

Compile the firmware:

```bash
esphome compile esp32-s3-dongle.yaml
```

If the ESP32-S3 is connected over USB, flash it directly:

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/ttyACM0
```

On macOS, the serial port is usually similar to:

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/cu.usbmodemXXXX
```

After the first flash, later updates can use OTA:

```bash
esphome upload esp32-s3-dongle.yaml
```

If the serial port cannot be found, check that the USB cable supports data and put the ESP32-S3 into boot/download mode.

`secrets.yaml` contains the WiFi password and is ignored by `.gitignore`. Do not commit it.
