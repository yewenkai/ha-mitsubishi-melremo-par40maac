# MELRemo / PAR-40MAAC Protocol Notes

[中文说明](protocol-notes-zh.md)

These notes are based on BLE HCI captures between an iPhone running MELRemo and a Mitsubishi Electric `PAR-40MAAC` panel. Only the parts needed by the current implementation are documented.

## GATT

Observed key handles:

- `0x0013`: firmware version read
- `0x0015`: software/model version read
- `0x0017`: request write without response
- `0x0019`: response notify
- `0x001a`: CCCD, write `0100` to enable notify

Example BLE address:

```text
28:e9:8e:xx:xx:xx
```

Example device name:

```text
M/RC_40MAAC_28E98EXXXXXX
```

## Frame Format

Full frame structure:

```text
length_le16 | message_id_u8 | payload | checksum_le16
```

Where:

- `length` is the length of `message_id + payload + checksum`.
- `message_id` increments and wraps.
- `checksum` is the 16-bit sum of all bytes in `length + message_id + payload`.
- 16-bit fields are little-endian.

## Authentication And Session

The PIN appears in authentication requests as a 16-bit little-endian value using a hex/BCD-like representation of the four displayed digits. For example, sample PIN `1234` is encoded as:

```text
34 12
```

Common authentication/session requests:

```text
0001 login
0003 session step
0401 session step
0403 logout step
0101 logout step
0103 logout step
0205 status request
0105 control request
```

## State And Control

Status request example:

```text
06 00 <id> 05 02 00 <checksum>
```

The control request payload is broadly compatible with the structure in the original `hass-mitsubishi_matouch` project:

```text
0501 | request_flag | flags_a | flags_b | flags_c | operation_mode_flags | setpoints... | vane_fan_mode | 00 | 00
```

The setpoint uses the original Mitsubishi temperature adapter, where a value such as `40 02` represents 24.0 C.

## Known Limits

- Only `PAR-40MAAC` has been tested directly.
- Other MELRemo-compatible panels may require additional captures.
- BLE connection failures usually happen before the protocol layer. Fix ESPHome Bluetooth Proxy placement, interference, or connection occupation first.
