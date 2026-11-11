#!/usr/bin/env bash

DIR="$HOME/Pictures/Screenshots"
mkdir -p "$DIR"
FILE="$DIR/screenshot_$(date +'%Y-%m-%d_%H-%M-%S').png"

if [ "$1" = "full" ]; then
    grim "$FILE"
    wl-copy < "$FILE"
    notify-send -a "Screenshot" -i "$FILE" "Full Screenshot Captured" "Saved to ~/Pictures/Screenshots and copied to clipboard."
else
    geometry=$(slurp 2>/dev/null)
    if [ -n "$geometry" ]; then
        grim -g "$geometry" "$FILE"
        wl-copy < "$FILE"
        notify-send -a "Screenshot" -i "$FILE" "Screenshot Captured" "Saved to ~/Pictures/Screenshots and copied to clipboard."
    fi
fi
