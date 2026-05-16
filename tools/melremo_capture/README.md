# MELRemo iPhone BLE Capture

[中文说明](README-zh.md)

This directory contains helper scripts for capturing BLE HCI traffic between iPhone MELRemo and a Mitsubishi `PAR-40MAAC` panel on a Mac.

## Requirements

- iPhone connected to the Mac over USB.
- iPhone is unlocked and trusts this Mac.
- Apple Bluetooth logging profile is installed on the iPhone.
- `idevicebtlogger` is installed on the Mac.
- Wireshark / tshark is installed on the Mac.

## Capture

```bash
chmod +x tools/melremo_capture/*.sh
tools/melremo_capture/start_ios_ble_capture.sh
```

After the command starts, open MELRemo and perform one operation at a time. Wait 3-5 seconds between operations.

Suggested sequence:

1. Connect to the panel.
2. Wait for the state to load.
3. Toggle power once.
4. Change operation mode once.
5. Adjust temperature by 1 degree.
6. Change fan speed once.
7. Change vane direction once.
8. Disconnect.

Press `Ctrl-C` in the terminal when finished.

## Extract ATT Plaintext

```bash
tools/melremo_capture/extract_att.sh captures/melremo/<capture>.pcap > captures/melremo/att.tsv
tools/melremo_capture/decode_frames.py captures/melremo/att.tsv > captures/melremo/frames.txt
```

Capture files may contain device addresses, PINs, or other private data. Do not publish raw captures by default.
