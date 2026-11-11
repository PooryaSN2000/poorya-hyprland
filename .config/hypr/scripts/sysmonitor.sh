#!/usr/bin/env bash
# Toggle System Monitor (Ptyxis + top)

if hyprctl clients -j | grep -q '"title": "System Resource Monitor"'; then
    hyprctl dispatch closewindow title:"System Resource Monitor"
else
    ptyxis -s --title="System Resource Monitor" -- top
fi
