#!/usr/bin/env bash
# Minimal Dock Toggle Script (Super + D)

DOCK_PID=$(pgrep -f "waybar -c .*dock.jsonc" | head -n 1)

if [ -n "$DOCK_PID" ]; then
    kill "$DOCK_PID"
else
    waybar -c /home/pooryasn/.config/waybar/dock.jsonc -s /home/pooryasn/.config/waybar/dock.css >/dev/null 2>&1 &
fi
