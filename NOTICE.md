# Notice

This project is derived from:

- Repository: `cyaneous/hass-mitsubishi_matouch`
- URL: https://github.com/cyaneous/hass-mitsubishi_matouch
- License: MIT

The original project provided the Home Assistant custom integration structure, BLE discovery metadata, entity implementation, and most MA Touch control model code.

This repository adds and documents changes verified against a Mitsubishi Electric `PAR-40MAAC` panel controlled by MELRemo:

- little-endian frame length, message type, PIN, and checksum handling
- 16-bit checksum handling
- unsolicited response tolerance and protocol debug logging
- ESPHome Bluetooth Proxy example
- iPhone/Mac MELRemo BLE capture helpers
- Chinese documentation and troubleshooting notes

Protocol analysis and implementation updates were completed with the assistance of Codex and OpenAI.
