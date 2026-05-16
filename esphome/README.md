# ESPHome 配置

本目录提供 ESP32-S3 Dongle 作为 Home Assistant Bluetooth Proxy 的示例配置。

使用前复制 secrets 模板：

```bash
cp secrets.yaml.example secrets.yaml
```

填写自己的 WiFi 信息后再编译或通过 ESPHome Dashboard 刷入：

```bash
docker compose -f docker-compose.esphome.linux.yml up -d
```

`secrets.yaml` 包含 WiFi 密码，已被 `.gitignore` 排除，不要提交。
