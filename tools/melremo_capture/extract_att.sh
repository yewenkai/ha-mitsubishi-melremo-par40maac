#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <capture.pcap>" >&2
  exit 1
fi

PCAP="$1"
TSHARK="/Applications/Wireshark.app/Contents/MacOS/tshark"

if [[ ! -f "${PCAP}" ]]; then
  echo "Capture file not found: ${PCAP}" >&2
  exit 1
fi

if [[ ! -x "${TSHARK}" ]]; then
  TSHARK="$(command -v tshark || true)"
fi

if [[ -z "${TSHARK}" ]]; then
  echo "tshark not found. Install Wireshark or add tshark to PATH." >&2
  exit 1
fi

"${TSHARK}" -r "${PCAP}" \
  -Y "btatt" \
  -T fields \
  -E header=y \
  -E separator=$'\t' \
  -e frame.number \
  -e frame.time_relative \
  -e bthci_acl.src.bd_addr \
  -e bthci_acl.dst.bd_addr \
  -e btatt.opcode \
  -e btatt.handle \
  -e btatt.uuid16 \
  -e btatt.uuid128 \
  -e btatt.value
