#!/usr/bin/env bash
# Toggle floating Scratchpad & Quick Todo window

if pgrep -f "[s]cratchpad_window.py" > /dev/null 2>&1; then
    pkill -f "[s]cratchpad_window.py"
else
    python3 /home/pooryasn/.config/hypr/scripts/scratchpad_window.py >/dev/null 2>&1 &
fi
