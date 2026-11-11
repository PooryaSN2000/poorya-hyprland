#!/usr/bin/env bash

# Minimal Beautiful Power Menu using Wofi
entries="󰌾  Lock Screen\n󰍃  Log Out\n󰒲  Suspend\n󰑓  Reboot\n󰐥  Shut Down"

selected=$(printf "%b\n" "$entries" | wofi --dmenu \
    --conf /home/pooryasn/.config/wofi/config \
    --style /home/pooryasn/.config/wofi/style.css \
    --prompt "Power Menu" \
    --width 280 \
    --height 270 \
    --hide-scroll)

case "$selected" in
    *"Lock"*)
        if command -v hyprlock >/dev/null 2>&1; then
            hyprlock
        elif command -v swaylock >/dev/null 2>&1; then
            swaylock
        else
            loginctl lock-session
        fi
        ;;
    *"Log Out"*)
        hyprctl dispatch exit
        ;;
    *"Suspend"*)
        systemctl suspend
        ;;
    *"Reboot"*)
        systemctl reboot
        ;;
    *"Shut Down"*)
        systemctl poweroff
        ;;
esac
