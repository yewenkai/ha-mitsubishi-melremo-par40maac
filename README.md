# Mitsubishi MELRemo PAR-40MAAC for Home Assistant

这是一个用于 Home Assistant 的三菱电机有线面板蓝牙控制实验项目，目标是通过 MELRemo（也常被写作 MEL Remo）蓝牙协议控制空调。

本项目基于并借鉴了 [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch) 的 Home Assistant 集成框架，在实际 `PAR-40MAAC` 面板和 MELRemo iPhone 抓包基础上修正了底层帧格式，使其可通过 Home Assistant + ESPHome Bluetooth Proxy 控制空调。

项目由用户实际设备调试，并在 Codex 与 OpenAI 协助下完成协议分析、代码修正和文档整理。

## 已验证设备

已验证：

- Mitsubishi Electric `PAR-40MAAC`
- BLE 名称形如 `M/RC_40MAAC_XXXXXXXXXXXX`
- MELRemo 可正常连接和控制的面板
- PIN 可通过面板显示，本项目测试时使用 `7777`

可能兼容但未验证：

- `PAR-4*MA`
- `PAR-4*MAAC`
- 其他支持 MELRemo 的 Mitsubishi MA Touch / MA remote 面板

如果你的设备能被 MELRemo 搜到，并且 Home Assistant 能通过蓝牙看到 `0277df18-e796-11e6-bf01-fe55135034f3` 服务 UUID，可以尝试本项目。

## 项目结构

```text
custom_components/mitsubishi_matouch/  Home Assistant 自定义集成
esphome/                               ESP32-S3 蓝牙中继示例配置
tools/melremo_capture/                 iPhone + Mac 抓取 MELRemo BLE 日志的工具
docs/                                  开发日志、协议笔记和排障说明
```

说明：Home Assistant 内部 domain 仍保留为 `mitsubishi_matouch`，这是为了兼容原项目结构和 HA 配置入口；仓库名称和展示名称已改为 `Mitsubishi MELRemo PAR-40MAAC`。

## 安装方式

### 方式一：手动安装

把 `custom_components/mitsubishi_matouch` 复制到 Home Assistant 配置目录：

```bash
cp -R custom_components/mitsubishi_matouch /config/custom_components/
```

然后重启 Home Assistant。

### 方式二：HACS 自定义仓库

在 HACS 中添加自定义仓库：

```text
https://github.com/yewenkai/ha-mitsubishi-melremo-par40maac
```

类别选择 `Integration`。

## 使用 ESPHome 蓝牙中继

如果 Home Assistant 主机离空调面板较远，可以使用 ESP32-S3 作为 Bluetooth Proxy。

本项目提供示例：

```text
esphome/esp32-s3-dongle.yaml
esphome/secrets.yaml.example
```

硬件可以选择常见的 ESP32-S3 Dongle 开发板，这类硬件可在淘宝购买。建议把 ESP32-S3 放在面板 0.5-1 米范围内，减少 BLE 建连失败。

ESPHome 核心配置如下：

```yaml
esp32_ble_tracker:
  scan_parameters:
    active: true

bluetooth_proxy:
  active: true
```

固件编译和刷机可以走 ESPHome 官方推荐的 Docker / Dashboard 路径，也可以用 conda 创建本地虚拟环境后执行 `esphome compile` 和 `esphome upload`。详细步骤见 [ESPHome 配置说明](esphome/README.md) 和 [ESPHome 蓝牙中继说明](docs/ESPHome蓝牙中继.md)。

不要把真实 `secrets.yaml` 提交到仓库。

## 添加设备

1. 关闭手机上的 MELRemo，避免同时连接面板。
2. 在面板上显示当前 PIN。
3. 确保面板处于主显示或状态显示。
4. 在 Home Assistant 中添加 `Mitsubishi MELRemo PAR-40MAAC`。
5. 选择或输入面板 MAC 地址。
6. 输入当前 PIN。

如果 PIN 改过，请以面板当前显示为准。

## 已修复的关键协议问题

原项目框架可复用，但在 `PAR-40MAAC` 实测中发现底层帧格式与代码不完全一致：

- 帧长度为 16 位 little-endian。
- 请求 message type 为 16 位 little-endian。
- PIN 为 16 位 little-endian。
- CRC/checksum 为 16 位求和 little-endian。
- 状态响应、控制响应通过 notify 特征返回。

本项目据 MELRemo 抓包修正了这些差异。

## 抓包与协议分析

如果遇到未支持面板，可以用 iPhone + Mac 抓取 MELRemo 与面板的 BLE 通讯：

```bash
brew install libimobiledevice
tools/melremo_capture/start_ios_ble_capture.sh
tools/melremo_capture/extract_att.sh captures/melremo/example.pcap > captures/melremo/att.tsv
tools/melremo_capture/decode_frames.py captures/melremo/att.tsv > captures/melremo/frames.txt
```

注意：抓包文件可能包含设备地址、PIN 或其他隐私信息，默认不要公开上传。

## 排障要点

- `ESP_GATT_CONN_FAIL_ESTABLISH` 通常是 BLE 建链失败，优先调整 ESP32-S3 与面板距离。
- MELRemo 和 Home Assistant 不要同时连接面板。
- 面板需要停留在主显示或状态显示。
- 如果提示 PIN 错误，重新在面板上查看当前 PIN。
- 如果能连接但不能控制，开启 `custom_components.mitsubishi_matouch` debug 日志并抓取 `SND` / `RCV`。

## 致谢与授权

本项目基于 MIT 协议项目 [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch) 修改而来，保留原项目授权声明。

感谢原作者提供 Home Assistant 集成框架、实体模型、蓝牙发现和控制结构。本项目主要补充 `PAR-40MAAC` / MELRemo 实测协议修正、ESPHome Bluetooth Proxy 使用说明和抓包工具。
