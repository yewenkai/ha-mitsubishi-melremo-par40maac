#!/usr/bin/env python3
"""Decode MELRemo ATT writes/notifications from an extracted GATT TSV file."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path


def iter_att_rows(path: Path):
    with path.open(newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:
            handle = row.get("btatt.handle", "")
            value = row.get("btatt.value", "")
            if not value:
                continue
            if handle == "0x0017":
                direction = "TX"
            elif handle == "0x0019":
                direction = "RX"
            else:
                continue
            yield (
                int(row["frame.number"]),
                float(row["frame.time_relative"]),
                direction,
                bytes.fromhex(value),
            )


def decode_frames(path: Path):
    buffers: dict[str, bytearray] = defaultdict(bytearray)
    starts: dict[str, tuple[int, float] | None] = defaultdict(lambda: None)

    for frame, ts, direction, data in iter_att_rows(path):
        if not buffers[direction]:
            starts[direction] = (frame, ts)

        buffers[direction].extend(data)

        while len(buffers[direction]) >= 2:
            length = int.from_bytes(buffers[direction][:2], "little")
            total = 2 + length
            if len(buffers[direction]) < total:
                break

            start_frame, start_ts = starts[direction] or (frame, ts)
            raw = bytes(buffers[direction][:total])
            del buffers[direction][:total]
            starts[direction] = (frame, ts) if buffers[direction] else None
            yield start_frame, start_ts, frame, ts, direction, raw


def describe_frame(raw: bytes) -> str:
    length = int.from_bytes(raw[:2], "little")
    message_id = raw[2]
    payload = raw[3:-2]
    crc = int.from_bytes(raw[-2:], "little")
    calculated_crc = sum(raw[:-2]) & 0xFFFF
    message_type = int.from_bytes(payload[:2], "little") if len(payload) >= 2 else None
    return (
        f"len={length:02d} id=0x{message_id:02x} "
        f"type=0x{message_type:04x} crc=0x{crc:04x}/0x{calculated_crc:04x} "
        f"payload={payload.hex()}"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <att.tsv>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    for start_frame, start_ts, end_frame, _end_ts, direction, raw in decode_frames(path):
        print(
            f"{start_frame:5d}-{end_frame:<5d} {start_ts:9.3f} "
            f"{direction} {describe_frame(raw)}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
