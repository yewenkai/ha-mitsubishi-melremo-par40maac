# 开发日志

[English](development-log.md)

## 2026-05-16

### 背景

目标是在 Home Assistant 中控制 Mitsubishi Electric `PAR-40MAAC` 面板对应的空调。面板可通过官方 iPhone 应用 MELRemo 正常控制，Home Assistant 侧使用 ESPHome Bluetooth Proxy 连接面板。

初始尝试使用 `cyaneous/hass-mitsubishi_matouch`，但出现以下问题：

- Home Assistant 报 `Unsolicited message received`
- ESPHome 日志偶发 `ESP_GATT_CONN_FAIL_ESTABLISH`
- 插件连接成功后仍无法稳定完成认证和状态读取

### 抓包

使用 iPhone + Mac 抓取 MELRemo 与 `PAR-40MAAC` 的 BLE HCI 通讯，并用 Wireshark / tshark 提取 ATT 数据。

抓包操作覆盖：

- 开机
- 调整温度
- 调整模式
- 调整风速
- 关机

抓包确认：

- 写特征 handle: `0x0017`
- 通知特征 handle: `0x0019`
- PIN 以 little-endian 16 位形式出现在认证报文中
- MELRemo 使用的协议帧可由原集成框架复用

### 协议修正

根据抓包，修正以下底层帧格式：

- header length 从 big-endian 改为 little-endian
- request message type 从 big-endian 改为 little-endian
- PIN 从 big-endian 改为 little-endian
- footer checksum 从 big-endian 改为 little-endian
- checksum 从 8 位求和改为 16 位求和

同时增加：

- 响应类型过滤，避免主动状态帧或迟到帧破坏当前请求
- unsolicited response 日志记录
- 响应 checksum 校验
- response timeout 从 5 秒提高到 15 秒，适配 ESPHome Bluetooth Proxy

### 项目整理

项目从原 `hass-mitsubishi_matouch` 整理为 `ha-mitsubishi-melremo-par40maac`，便于用户通过以下关键词搜索：

- Mitsubishi
- MELRemo
- PAR-40MAAC
- Home Assistant
- ESPHome Bluetooth Proxy

仓库内容分为：

- Home Assistant 自定义集成
- ESPHome 蓝牙中继配置
- iPhone/Mac 抓包工具
- 英文默认文档和中文 `-zh` 文档

### 隐私处理

发布前排除了以下内容：

- WiFi SSID 和密码
- Home Assistant 配置库
- 抓包原始文件
- 编译固件
- 本地日志
- `__pycache__`
