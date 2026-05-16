# MELRemo / PAR-40MAAC 协议笔记

[English](protocol-notes.md)

这份笔记来自 `PAR-40MAAC` 面板与 iPhone MELRemo 的 BLE HCI 抓包，仅记录目前实现需要的部分。

## GATT

已观察到的关键 handle：

- `0x0013`: firmware version read
- `0x0015`: software/model version read
- `0x0017`: request write without response
- `0x0019`: response notify
- `0x001a`: CCCD，写入 `0100` 开启 notify

设备 BLE 地址示例：

```text
28:e9:8e:xx:xx:xx
```

设备名称示例：

```text
M/RC_40MAAC_28E98EXXXXXX
```

## 帧格式

完整帧结构：

```text
length_le16 | message_id_u8 | payload | checksum_le16
```

其中：

- `length` 是 `message_id + payload + checksum` 的长度。
- `message_id` 递增并循环。
- `checksum` 是 `length + message_id + payload` 所有字节求和后取 16 位。
- 16 位字段使用 little-endian。

## 认证和会话

PIN 在认证请求中以四位显示数字的十六进制/BCD 风格放入 16 位 little-endian 字段。例如示例 PIN `1234` 表现为：

```text
34 12
```

常见认证/会话请求：

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

## 状态与控制

状态请求示例：

```text
06 00 <id> 05 02 00 <checksum>
```

控制请求的 payload 与原 `hass-mitsubishi_matouch` 中的结构基本一致，可复用：

```text
0501 | request_flag | flags_a | flags_b | flags_c | operation_mode_flags | setpoints... | vane_fan_mode | 00 | 00
```

其中 setpoint 使用原项目的 Mitsubishi temperature adapter，即类似 `40 02` 表示 24.0。

## 已知限制

- 目前只用 `PAR-40MAAC` 实测验证。
- 其他 MELRemo 支持的面板可能还需要抓包确认。
- BLE 建链失败通常发生在协议层之前，需要先解决 ESPHome Bluetooth Proxy 与面板的距离、干扰或连接占用问题。
