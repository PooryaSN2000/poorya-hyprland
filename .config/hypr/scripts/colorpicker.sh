#!/usr/bin/env bash
# Hyprpicker wrapper with notification & auto-copy (Super + Shift + C)

COLOR=$(hyprpicker -a -n)

if [ -n "$COLOR" ]; then
    notify-send -a "Color Picker" -i "accessories-character-map" "Color Copied: $COLOR" "Value stored in clipboard."
fi
