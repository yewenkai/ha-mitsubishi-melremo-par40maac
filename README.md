# Mitsubishi MELRemo PAR-40MAAC for Home Assistant

[中文说明](README-zh.md)

This is an experimental Home Assistant custom integration for controlling Mitsubishi Electric wired controller panels over Bluetooth through the MELRemo, also written as MEL Remo, protocol.

The project is based on and derived from [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch). It keeps the original Home Assistant integration structure and applies protocol fixes verified with a real `PAR-40MAAC` panel and MELRemo iPhone BLE captures, so the air conditioner can be controlled through Home Assistant and an ESPHome Bluetooth Proxy.

The protocol analysis, code changes, and documentation were completed on real hardware with assistance from Codex and OpenAI.

## Disclaimer

This project is provided for non-commercial learning, research, interoperability, and personal automation on equipment you own or are authorized to operate.

It is not affiliated with, endorsed by, sponsored by, or supported by Mitsubishi Electric or any of its affiliates. Mitsubishi Electric, MELRemo, MEL Remo, MA Touch, and related names may be trademarks of their respective owners.

Do not use this project to access, interfere with, damage, bypass security controls on, or operate any computer system, building system, HVAC system, Bluetooth device, or network that you do not own or have explicit permission to use. This project is not intended to attack, intrude into, or impair Mitsubishi Electric systems or any third-party system.

The software is provided as-is, without warranty. You are responsible for complying with local laws, safety requirements, device warranty terms, building management rules, and any applicable service terms. HVAC control can affect comfort, energy usage, and equipment operation; use it carefully.

## Verified Hardware

Verified:

- Mitsubishi Electric `PAR-40MAAC`
- BLE name in the form `M/RC_40MAAC_XXXXXXXXXXXX`
- Panels that can be connected and controlled by MELRemo
- The PIN is shown on the panel and must be entered during setup

Panel reference:

- [PAR-40MAA wall mounted controller - Mitsubishi Electric Australia](https://www.mitsubishielectric.com.au/product/par-40maa-wall-mounted-controller/)

Possibly compatible but not verified:

- `PAR-4*MA`
- `PAR-4*MAAC`
- Other Mitsubishi MA Touch / MA remote panels supported by MELRemo

If your device is visible in MELRemo and Home Assistant can see the service UUID `0277df18-e796-11e6-bf01-fe55135034f3`, this integration may be worth trying.

## Repository Layout

```text
custom_components/mitsubishi_matouch/  Home Assistant custom integration
esphome/                               ESP32-S3 Bluetooth Proxy example
tools/melremo_capture/                 iPhone + Mac MELRemo BLE capture helpers
docs/                                  development log, protocol notes, troubleshooting
```

The internal Home Assistant domain remains `mitsubishi_matouch` for compatibility with the original integration and Home Assistant config flow. The repository and display name are changed to `Mitsubishi MELRemo PAR-40MAAC`.

## Installation

### Manual Install

Copy the custom component into your Home Assistant config directory:

```bash
cp -R custom_components/mitsubishi_matouch /config/custom_components/
```

Then restart Home Assistant.

### HACS Custom Repository

Add this repository to HACS as a custom repository:

```text
https://github.com/yewenkai/ha-mitsubishi-melremo-par40maac
```

Select `Integration` as the category.

## ESPHome Bluetooth Proxy

If the Home Assistant host is not close enough to the air conditioner panel, use an ESP32-S3 as a Bluetooth Proxy.

Examples are included:

```text
esphome/esp32-s3-dongle.yaml
esphome/secrets.yaml.example
```

Common ESP32-S3 Dongle boards can be purchased from Taobao. Place the ESP32-S3 around 0.5-1 m from the panel when possible to reduce BLE connection failures.

The key ESPHome configuration is:

```yaml
esp32_ble_tracker:
  scan_parameters:
    active: true

bluetooth_proxy:
  active: true
```

Firmware compilation and flashing can use either the official Docker / ESPHome Dashboard path or a local conda virtual environment with `esphome compile` and `esphome upload`.

See:

- [ESPHome firmware guide](esphome/README.md)
- [ESPHome Bluetooth Proxy notes](docs/esphome-bluetooth-proxy.md)
- [中文 ESPHome 固件说明](esphome/README-zh.md)
- [中文 ESPHome 蓝牙中继说明](docs/esphome-bluetooth-proxy-zh.md)

Do not commit a real `secrets.yaml` file.

## Add A Device

1. Close MELRemo on your phone so it does not keep the panel connection.
2. Show the current PIN on the panel.
3. Keep the panel on its main or status screen.
4. Add `Mitsubishi MELRemo PAR-40MAAC` in Home Assistant.
5. Select or enter the panel MAC address.
6. Enter the current PIN.

If the PIN was changed, always use the PIN currently shown by the panel.

## Practical Use Cases

After the air conditioner is available as a Home Assistant climate entity, it can be combined with other Home Assistant integrations and automations.

### Siri And Apple Home

With the Home Assistant HomeKit Bridge integration, the air conditioner entity can be exposed to Apple Home. After that, Siri can be used for commands such as turning the air conditioner on or off, subject to how the entity is named and exposed in HomeKit Bridge.

The Home Assistant climate entity supports setting the fan speed to `auto`, but the Apple Home app usually does not expose "auto fan speed" as a selectable option in its air-conditioner UI. If you want to trigger auto fan speed from Apple Home, create a Home Assistant script and expose that script through HomeKit Bridge as a scene or switch:

```yaml
script:
  mitsubishi_set_auto_fan:
    alias: Mitsubishi AC Auto Fan
    sequence:
      - service: climate.set_fan_mode
        target:
          entity_id: climate.mitsubishi_aircon
        data:
          fan_mode: auto
```

Replace `climate.mitsubishi_aircon` with your air-conditioner entity ID. Then include `script.mitsubishi_set_auto_fan` in HomeKit Bridge so Apple Home or Siri can indirectly set auto fan speed.

If there is an Apple TV, HomePod, or similar Apple home hub in the home, the Apple Home app on iPhone can usually control the air conditioner remotely through Apple's HomeKit remote access. Another option is to expose Home Assistant securely to the internet, for example through a VPN, HTTPS reverse proxy, or another trusted remote access method, and then control the air conditioner through Home Assistant while away from home.

Avoid exposing Home Assistant directly to the public internet without authentication, HTTPS, and proper network protection.

### Simple Temperature Automation

This integration can also work with a temperature sensor, such as a Mijia thermometer already connected to Home Assistant, to build simple comfort automations.

For example:

- When the iPhone is detected at home, it is nighttime, and the room temperature stays above a configured threshold for a period of time, Home Assistant can turn on the air conditioner automatically to avoid waking up from heat.
- When turning on the air conditioner, Home Assistant can also turn off an existing Mijia fan or another fan that is already connected to Home Assistant.
- If the room temperature becomes too low for a period of time, Home Assistant can turn the air conditioner off automatically, although this may not be necessary in every home.

Treat these automations as examples only. Tune thresholds, delays, and safety conditions for your own room, sensor placement, and air conditioner behavior.

## Key Protocol Fixes

The original integration structure is reusable, but the tested `PAR-40MAAC` panel uses different low-level frame details:

- Frame length is 16-bit little-endian.
- Request message type is 16-bit little-endian.
- PIN is 16-bit little-endian.
- CRC/checksum is a 16-bit little-endian byte sum.
- Status and control responses are returned through the notify characteristic.

These differences were fixed based on MELRemo BLE captures.

## Capture And Protocol Analysis

For unsupported panels, an iPhone and Mac can be used to capture BLE traffic between MELRemo and the panel:

```bash
brew install libimobiledevice
tools/melremo_capture/start_ios_ble_capture.sh
tools/melremo_capture/extract_att.sh captures/melremo/example.pcap > captures/melremo/att.tsv
tools/melremo_capture/decode_frames.py captures/melremo/att.tsv > captures/melremo/frames.txt
```

Capture files may contain device addresses, PINs, or other private data. Do not publish raw captures by default.

See:

- [Protocol notes](docs/protocol-notes.md)
- [Development log](docs/development-log.md)
- [MELRemo capture guide](tools/melremo_capture/README.md)
- [中文协议笔记](docs/protocol-notes-zh.md)
- [中文开发日志](docs/development-log-zh.md)
- [中文抓包说明](tools/melremo_capture/README-zh.md)

## Related Work

This project follows the Mitsubishi Electric MELRemo / MA Remote local Bluetooth control path. It is different from MELCloud cloud control, CN105 indoor-unit serial control, and infrared remote-control solutions.

- [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch): the Home Assistant integration framework directly referenced and modified by this project, targeting Mitsubishi MA Touch BLE thermostats.
- [Home Assistant MELCloud](https://www.home-assistant.io/integrations/melcloud/): the official Home Assistant integration for MELCloud enabled devices. It depends on the MELCloud ecosystem.
- [pymitsubishi/homeassistant-mitsubishi](https://github.com/pymitsubishi/homeassistant-mitsubishi): a local network control approach for Mitsubishi MAC-577IF-2E / MAC-587 Wi-Fi adapter based installations.
- [echavet/MitsubishiCN105ESPHome](https://github.com/echavet/MitsubishiCN105ESPHome): an ESPHome + CN105 serial-port approach that connects directly to the indoor unit control board.
- Infrared remote-control solutions, such as [BroadLink](https://www.home-assistant.io/integrations/broadlink/) or ESPHome IR, are easier to deploy but usually cannot reliably read the air conditioner's real state.

The focus of this project is to integrate BLE-capable MA Remote panels through the MELRemo Bluetooth protocol without opening the indoor unit and without depending on MELCloud, then expose the panel as a Home Assistant climate entity.

## Troubleshooting

- `ESP_GATT_CONN_FAIL_ESTABLISH` usually means BLE connection establishment failed before the protocol layer. Move the ESP32-S3 closer to the panel first.
- Do not keep MELRemo and Home Assistant connected to the panel at the same time.
- Keep the panel on its main or status screen.
- If the setup reports a PIN error, check the current PIN on the panel again.
- If the integration connects but cannot control the unit, enable debug logging for `custom_components.mitsubishi_matouch` and inspect `SND` / `RCV` logs.

## Credits And License

This project is derived from the MIT-licensed [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch) project and preserves the original license notice.

Thanks to the original author for the Home Assistant integration framework, entity model, Bluetooth discovery code, and MA Touch control model. This repository mainly adds `PAR-40MAAC` / MELRemo protocol fixes, ESPHome Bluetooth Proxy notes, capture helpers, and bilingual documentation.
