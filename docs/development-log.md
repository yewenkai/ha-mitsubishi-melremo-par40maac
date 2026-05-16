# Development Log

[中文说明](development-log-zh.md)

## 2026-05-16

### Background

The goal was to control an air conditioner through Home Assistant by talking to a Mitsubishi Electric `PAR-40MAAC` wired controller. The panel can already be controlled by the official iPhone app MELRemo, while Home Assistant connects through an ESPHome Bluetooth Proxy.

The initial attempt used `cyaneous/hass-mitsubishi_matouch`, but several issues appeared:

- Home Assistant logged `Unsolicited message received`.
- ESPHome occasionally logged `ESP_GATT_CONN_FAIL_ESTABLISH`.
- Even after BLE connection succeeded, authentication and state reads were not stable.

### Capture

BLE HCI traffic between MELRemo and the `PAR-40MAAC` panel was captured using an iPhone and Mac, then ATT data was extracted with Wireshark / tshark.

Captured operations included:

- Power on
- Temperature adjustment
- Mode adjustment
- Fan speed adjustment
- Power off

The capture confirmed:

- Write characteristic handle: `0x0017`
- Notify characteristic handle: `0x0019`
- PIN is encoded as a 16-bit little-endian value in the authentication frame
- The original integration's protocol model can be reused after low-level frame fixes

### Protocol Fixes

The capture showed these low-level frame changes were needed:

- Header length changed from big-endian to little-endian.
- Request message type changed from big-endian to little-endian.
- PIN changed from big-endian to little-endian.
- Footer checksum changed from big-endian to little-endian.
- Checksum changed from 8-bit byte sum to 16-bit byte sum.

Additional changes:

- Response type filtering to prevent unsolicited or delayed frames from breaking the active request.
- Logging for unsolicited responses.
- Incoming checksum validation.
- Response timeout increased from 5 seconds to 15 seconds for ESPHome Bluetooth Proxy.

### Project Cleanup

The project was reorganized from the original `hass-mitsubishi_matouch` name to `ha-mitsubishi-melremo-par40maac` so it can be found through these keywords:

- Mitsubishi
- MELRemo
- MEL Remo
- PAR-40MAAC
- Home Assistant
- ESPHome Bluetooth Proxy

Repository sections:

- Home Assistant custom integration
- ESPHome Bluetooth Proxy configuration
- iPhone/Mac capture helpers
- English and Chinese documentation

### Privacy Handling

Before publishing, these items were excluded:

- WiFi SSID and password
- Home Assistant configuration database
- Raw capture files
- Compiled firmware
- Local logs
- `__pycache__`
