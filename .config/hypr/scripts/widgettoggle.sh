#!/usr/bin/env bash
# Toggle Live Desktop Widget

PID=$(pgrep -f "python3 .*desktop_widget.py" | head -n 1)

if [ -n "$PID" ]; then
    kill "$PID"
else
    python3 /home/pooryasn/.config/hypr/scripts/desktop_widget.py >/dev/null 2>&1 &
fi
