#!/usr/bin/env bash

if pgrep -x wf-recorder >/dev/null 2>&1; then
    echo '{"text": "󰑋 REC", "tooltip": "Screen recording in progress.\nClick to stop and save.", "class": "recording"}'
else
    echo '{"text": "", "tooltip": "", "class": "idle"}'
fi
