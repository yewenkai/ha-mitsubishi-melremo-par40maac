# ESPHome 配置与固件编译

[English](README.md)

本目录提供 ESP32-S3 Dongle 作为 Home Assistant Bluetooth Proxy 的示例配置。

使用前复制 secrets 模板：

```bash
cp secrets.yaml.example secrets.yaml
```

填写自己的 WiFi 信息后再编译或通过 ESPHome Dashboard 刷入。

## 路径一：官方推荐 Docker / ESPHome Dashboard

在 Linux 主机上可以用 Docker 运行 ESPHome Dashboard：

```bash
docker compose -f docker-compose.esphome.linux.yml up -d
```

然后在 Dashboard 中导入或编辑 `esp32-s3-dongle.yaml`，完成编译和 OTA。

如果设备首次刷机，需要把 ESP32-S3 通过 USB 接到可访问串口的电脑或主机，并按 ESPHome Dashboard 提示刷入。

## 路径二：conda 虚拟环境本地编译

也可以使用 conda 创建独立 Python 环境：

```bash
conda create -n esphome python=3.12 -y
conda activate esphome
pip install esphome
```

检查配置：

```bash
esphome config esp32-s3-dongle.yaml
```

编译固件：

```bash
esphome compile esp32-s3-dongle.yaml
```

如果 ESP32-S3 已经接入 USB，可直接刷机：

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/ttyACM0
```

macOS 下串口通常类似：

```bash
esphome upload esp32-s3-dongle.yaml --device /dev/cu.usbmodemXXXX
```

首次刷机后，后续可以走 OTA：

```bash
esphome upload esp32-s3-dongle.yaml
```

如果刷机时找不到串口，先确认 USB 线支持数据传输，并让 ESP32-S3 进入 boot/download 模式。

`secrets.yaml` 包含 WiFi 密码，已被 `.gitignore` 排除，不要提交。
