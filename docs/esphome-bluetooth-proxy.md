# ESPHome Bluetooth Proxy

[中文说明](esphome-bluetooth-proxy-zh.md)

This project can use an ESPHome Bluetooth Proxy to let Home Assistant connect to a `PAR-40MAAC` panel indirectly.

## Hardware

An ESP32-S3 Dongle or a similar ESP32-S3 development board is recommended. These boards are commonly available from Taobao.

Recommendations:

- Place it near the air conditioner panel, preferably within 0.5-1 m.
- Avoid USB 3.0 ports, routers, power adapters, and metal obstructions.
- If you power it through a USB extension cable, keep the ESP32-S3 itself close to the panel.

## Configuration

Example configuration:

```text
esphome/esp32-s3-dongle.yaml
```

Copy the secrets template:

```bash
cp esphome/secrets.yaml.example esphome/secrets.yaml
```

Then enter your own WiFi information. Do not commit the real `secrets.yaml` file.

Key configuration:

```yaml
esp32_ble_tracker:
  scan_parameters:
    active: true

bluetooth_proxy:
  active: true
```

## Compile And Flash Paths

There are two practical paths.

### Official Docker / Dashboard Path

Use Docker or ESPHome Dashboard:

```bash
docker compose -f esphome/docker-compose.esphome.linux.yml up -d
```

Then compile, download, or flash the firmware from the Dashboard.

### Local Conda Path

If you do not want to use Docker, create an isolated conda environment:

```bash
cd esphome
conda create -n esphome python=3.12 -y
conda activate esphome
pip install esphome
esphome config esp32-s3-dongle.yaml
esphome compile esp32-s3-dongle.yaml
```

USB flashing example:

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/ttyACM0
```

On macOS, the serial port is usually similar to:

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/cu.usbmodemXXXX
```

After the first successful USB flash and WiFi connection, later updates can use OTA:

```bash
esphome upload esp32-s3-dongle.yaml
```

## Home Assistant

After the ESPHome device is online, Home Assistant should discover a remote Bluetooth adapter. When this integration is added, Home Assistant can connect to the panel through that Bluetooth Proxy.

## Common Issues

### `ESP_GATT_CONN_FAIL_ESTABLISH`

This is a BLE connection establishment failure before the protocol layer. Check these first:

- Move the ESP32-S3 closer to the panel.
- Close MELRemo.
- Restart the ESP32-S3.
- Restart Home Assistant.
- Keep the panel on the main or status screen.

### Device Is Discovered But Setup Fails

Check:

- Whether the PIN is the current PIN shown by the panel.
- Whether the panel is occupied by MELRemo on a phone.
- Whether Home Assistant logs contain `SND` / `RCV`.

If there is no `SND` / `RCV`, the integration has not reached the protocol layer yet.
