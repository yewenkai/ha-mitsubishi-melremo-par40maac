# ESPHome 蓝牙中继说明

本项目可以通过 ESPHome Bluetooth Proxy 让 Home Assistant 间接连接 `PAR-40MAAC` 面板。

## 硬件

推荐使用 ESP32-S3 Dongle 或类似 ESP32-S3 开发板。这类硬件可以在淘宝购买。

建议：

- 放在空调面板附近，优先 0.5-1 米范围。
- 尽量避开 USB 3.0 口、路由器、电源适配器和金属遮挡。
- 如果使用 USB 延长线供电，尽量把 ESP32-S3 本体靠近面板。

## 配置

示例配置：

```text
esphome/esp32-s3-dongle.yaml
```

需要复制：

```bash
cp esphome/secrets.yaml.example esphome/secrets.yaml
```

然后填写自己的 WiFi 信息。不要提交真实 `secrets.yaml`。

核心配置：

```yaml
esp32_ble_tracker:
  scan_parameters:
    active: true

bluetooth_proxy:
  active: true
```

## 编译和刷机路径

可以走两条路径。

### 官方推荐路径

使用 Docker 或 ESPHome Dashboard：

```bash
docker compose -f esphome/docker-compose.esphome.linux.yml up -d
```

然后在 Dashboard 中编译、下载或刷入固件。

### conda 本地路径

如果不想使用 Docker，也可以用 conda 创建独立环境：

```bash
cd esphome
conda create -n esphome python=3.12 -y
conda activate esphome
pip install esphome
esphome config esp32-s3-dongle.yaml
esphome compile esp32-s3-dongle.yaml
```

USB 刷机示例：

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/ttyACM0
```

macOS 串口通常是：

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/cu.usbmodemXXXX
```

首次刷机成功并接入 WiFi 后，后续可以直接 OTA：

```bash
esphome upload esp32-s3-dongle.yaml
```

## Home Assistant

ESPHome 设备上线后，Home Assistant 会发现一个远端蓝牙适配器。之后添加本项目集成时，HA 会通过这个 Bluetooth Proxy 连接面板。

## 常见问题

### `ESP_GATT_CONN_FAIL_ESTABLISH`

这是 BLE 建链失败，发生在本项目协议层之前。优先处理：

- ESP32-S3 靠近面板
- 关闭 MELRemo
- 重启 ESP32-S3
- 重启 Home Assistant
- 确认面板显示主显示或状态显示

### 能发现设备但无法添加

检查：

- PIN 是否为面板当前显示的 PIN
- 面板是否被手机 MELRemo 占用
- Home Assistant 日志里是否出现 `SND` / `RCV`

如果没有 `SND` / `RCV`，说明还没进入协议层。
