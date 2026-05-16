#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="${ROOT_DIR}/captures/melremo"
TS="$(date +%Y%m%d-%H%M%S)"
OUT_FILE="${OUT_DIR}/melremo-ios-${TS}.pcap"

mkdir -p "${OUT_DIR}"

if ! command -v idevicebtlogger >/dev/null 2>&1; then
  echo "idevicebtlogger not found. Install with: brew install libimobiledevice" >&2
  exit 1
fi

UDIDS="$(idevice_id -l || true)"
if [[ -z "${UDIDS}" ]]; then
  cat >&2 <<'MSG'
No iPhone detected.

Connect the iPhone by USB, unlock it, tap Trust This Computer, and run again.
The iPhone also needs Apple's Bluetooth logging profile installed.
MSG
  exit 1
fi

UDID="$(echo "${UDIDS}" | head -n 1)"

cat <<MSG
Writing iPhone Bluetooth HCI capture to:
  ${OUT_FILE}

Use MELRemo now:
  1. Connect to MA Touch / PAR-40MAAC.
  2. Wait until the current status is visible.
  3. Perform one action at a time: power, mode, temperature, fan, vane.
  4. Wait 3-5 seconds between actions.

Press Ctrl-C here when finished.
MSG

idevicebtlogger -u "${UDID}" -f pcap "${OUT_FILE}"
