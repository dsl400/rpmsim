#!/bin/bash

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)"

FIRMWARE_PATH="${SCRIPT_PATH}/lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-16.bin"

python -m esptool --chip esp32s3 -p /dev/ttyACM0 -b 460800 write-flash --flash-mode dio --flash-size 16MB --flash-freq 80m --erase-all 0x0 "${FIRMWARE_PATH}"
