# MELRemo iPhone BLE 抓包

[English](README.md)

这个目录用于在 Mac 上抓取 iPhone MELRemo 与 Mitsubishi `PAR-40MAAC` 面板之间的 BLE HCI 通讯。

## 前提

- iPhone 通过 USB 连接 Mac。
- iPhone 已解锁并信任这台 Mac。
- iPhone 已安装 Apple Bluetooth logging profile。
- Mac 已安装 `idevicebtlogger`。
- Mac 已安装 Wireshark / tshark。

## 抓包

```bash
chmod +x tools/melremo_capture/*.sh
tools/melremo_capture/start_ios_ble_capture.sh
```

命令运行后，打开 MELRemo，一次只做一个操作，每个操作之间等待 3-5 秒。

建议顺序：

1. 连接面板。
2. 等待状态显示出来。
3. 开/关一次。
4. 改一次运行模式。
5. 温度调整 1 度。
6. 改一次风速。
7. 改一次风向。
8. 断开连接。

完成后在终端按 `Ctrl-C`。

## 提取 ATT 明文

```bash
tools/melremo_capture/extract_att.sh captures/melremo/<capture>.pcap > captures/melremo/att.tsv
tools/melremo_capture/decode_frames.py captures/melremo/att.tsv > captures/melremo/frames.txt
```

注意：抓包文件可能包含设备地址、PIN 或其他隐私信息，默认不要公开上传。
