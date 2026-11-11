#!/usr/bin/env bash
# Native Hyprland Night Light Toggle (Super + Shift + N)

SHADER="$HOME/.config/hypr/shaders/nightlight.frag"
CURRENT=$(hyprctl getoption decoration:screen_shader -j | jq -r '.str')

if [ -z "$CURRENT" ] || [ "$CURRENT" = "[[EMPTY]]" ]; then
    hyprctl keyword decoration:screen_shader "$SHADER"
    notify-send -a "Night Light" -i "weather-clear-night" "Night Light: ON" "Warm 3800K filter activated."
else
    hyprctl keyword decoration:screen_shader ""
    notify-send -a "Night Light" -i "display-brightness-symbolic" "Night Light: OFF" "Standard color temperature restored."
fi
