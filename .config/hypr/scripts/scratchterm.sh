#!/usr/bin/env bash
# Quake-style dropdown scratchpad terminal

# Check if scratchterm window exists
if ! hyprctl clients -j | grep -q '"title": "scratchterm"'; then
    # Start scratchterm into special workspace
    hyprctl dispatch -- exec [workspace special:terminal] ptyxis -s --title="scratchterm"
    sleep 0.3
fi

hyprctl dispatch togglespecialworkspace terminal
