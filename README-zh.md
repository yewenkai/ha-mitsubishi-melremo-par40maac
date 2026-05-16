# Mitsubishi MELRemo PAR-40MAAC for Home Assistant

[English](README.md)

这是一个用于 Home Assistant 的三菱电机有线面板蓝牙控制实验项目，目标是通过 MELRemo（也常被写作 MEL Remo）蓝牙协议控制空调。

本项目基于并借鉴了 [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch) 的 Home Assistant 集成框架，在实际 `PAR-40MAAC` 面板和 MELRemo iPhone 抓包基础上修正了底层帧格式，使其可通过 Home Assistant + ESPHome Bluetooth Proxy 控制空调。

项目由用户实际设备调试，并在 Codex 与 OpenAI 协助下完成协议分析、代码修正和文档整理。

## 免责声明

本项目仅用于非商业目的下的学习、研究、互操作验证和个人自有设备自动化控制。

本项目与 Mitsubishi Electric（三菱电机）及其关联公司不存在从属、授权、赞助或官方支持关系。Mitsubishi Electric、MELRemo、MEL Remo、MA Touch 等名称可能是其各自权利人的商标。

请不要使用本项目访问、干扰、破坏、绕过安全控制或操作任何你不拥有且未获得明确授权的计算机系统、楼宇系统、暖通空调系统、蓝牙设备或网络。本项目无意攻击、侵入或损害三菱电机系统或任何第三方系统。

本项目按现状提供，不提供任何明示或默示担保。使用者需要自行确认当地法律法规、设备保修条款、楼宇管理要求和相关服务条款。空调控制可能影响舒适度、能耗和设备运行，请谨慎使用。

## 已验证设备

已验证：

- Mitsubishi Electric `PAR-40MAAC`
- BLE 名称形如 `M/RC_40MAAC_XXXXXXXXXXXX`
- MELRemo 可正常连接和控制的面板
- PIN 可通过面板显示，安装时填写自己面板上的 PIN

面板参考页面：

- [PAR-40MAA wall mounted controller - Mitsubishi Electric Australia](https://www.mitsubishielectric.com.au/product/par-40maa-wall-mounted-controller/)

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

固件编译和刷机可以走 ESPHome 官方推荐的 Docker / Dashboard 路径，也可以用 conda 创建本地虚拟环境后执行 `esphome compile` 和 `esphome upload`。详细步骤见 [ESPHome 配置说明](esphome/README-zh.md) 和 [ESPHome 蓝牙中继说明](docs/esphome-bluetooth-proxy-zh.md)。

不要把真实 `secrets.yaml` 提交到仓库。

## 添加设备

1. 关闭手机上的 MELRemo，避免同时连接面板。
2. 在面板上显示当前 PIN。
3. 确保面板处于主显示或状态显示。
4. 在 Home Assistant 中添加 `Mitsubishi MELRemo PAR-40MAAC`。
5. 选择或输入面板 MAC 地址。
6. 输入当前 PIN。

如果 PIN 改过，请以面板当前显示为准。

## 实际应用场景

空调接入 Home Assistant 并形成 climate 实体后，可以继续和 Home Assistant 的其他集成、自动化能力配合使用。

### Siri 和 Apple 家庭

配合 Home Assistant 的 HomeKit Bridge 集成，可以把空调实体暴露到 Apple 家庭。之后就可以通过 Siri 执行类似“打开空调”“关闭空调”的语音控制，具体效果取决于实体名称和 HomeKit Bridge 中暴露的实体类型。

如果家里有 Apple TV、HomePod 等 Apple 家庭中枢，iPhone 上的“家庭”App 通常可以通过 Apple 的 HomeKit 远程访问能力，在外面控制家中的空调。另一种方式是安全地把 Home Assistant 暴露到公网，例如通过 VPN、HTTPS 反向代理或其他可信远程访问方案，然后在外面通过 Home Assistant 控制空调。

不要在缺少认证、HTTPS 和网络防护的情况下直接把 Home Assistant 暴露到公网。

### 简单温度自动化

本项目也可以和已经接入 Home Assistant 的温度传感器配合，例如米家温度计，用来做一些简单的舒适度自动化。

例如：

- 当 iPhone 被判断为在家、当前是夜间，并且房间温度持续一段时间高于设定阈值时，Home Assistant 可以自动打开空调，避免睡觉时被热醒。
- 打开空调的同时，也可以自动关闭已经接入 Home Assistant 的米家电风扇或其他电风扇。
- 如果房间温度持续一段时间低于设定阈值，也可以自动关闭空调，不过这个规则不一定每个家庭都需要。

这些自动化只是示例。实际使用时需要根据房间大小、传感器位置、空调响应速度和个人体感，调整温度阈值、持续时间和安全条件。

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

## 相关项目

本项目属于 Mitsubishi Electric MELRemo / MA Remote 蓝牙本地控制路线，区别于 MELCloud 云端控制、CN105 主板串口控制和红外遥控方案。

- [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch)：本项目直接借鉴并修改的 Home Assistant 集成框架，面向 Mitsubishi MA Touch BLE thermostats。
- [Home Assistant MELCloud](https://www.home-assistant.io/integrations/melcloud/)：官方 Home Assistant 集成，适用于 MELCloud enabled devices，依赖 MELCloud 生态。
- [pymitsubishi/homeassistant-mitsubishi](https://github.com/pymitsubishi/homeassistant-mitsubishi)：面向 MAC-577IF-2E / MAC-587 Wi-Fi adapter 的本地网络控制方案。
- [echavet/MitsubishiCN105ESPHome](https://github.com/echavet/MitsubishiCN105ESPHome)：通过 ESPHome + CN105 串口直连空调内机主板的方案。
- 红外遥控方案：如 [BroadLink](https://www.home-assistant.io/integrations/broadlink/) / ESPHome IR，部署简单，但通常无法可靠读取空调真实状态。

本项目的重点是：在不拆内机、不依赖 MELCloud 的情况下，通过 MELRemo 蓝牙协议接入支持 BLE 的 MA Remote 面板，并将其暴露为 Home Assistant climate 实体。

## 排障要点

- `ESP_GATT_CONN_FAIL_ESTABLISH` 通常是 BLE 建链失败，优先调整 ESP32-S3 与面板距离。
- MELRemo 和 Home Assistant 不要同时连接面板。
- 面板需要停留在主显示或状态显示。
- 如果提示 PIN 错误，重新在面板上查看当前 PIN。
- 如果能连接但不能控制，开启 `custom_components.mitsubishi_matouch` debug 日志并抓取 `SND` / `RCV`。

## 致谢与授权

本项目基于 MIT 协议项目 [cyaneous/hass-mitsubishi_matouch](https://github.com/cyaneous/hass-mitsubishi_matouch) 修改而来，保留原项目授权声明。

感谢原作者提供 Home Assistant 集成框架、实体模型、蓝牙发现和控制结构。本项目主要补充 `PAR-40MAAC` / MELRemo 实测协议修正、ESPHome Bluetooth Proxy 使用说明和抓包工具。
