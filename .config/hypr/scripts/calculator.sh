#!/usr/bin/env bash
# Instant floating calculator toggle for Hyprland

if pidof gnome-calculator > /dev/null 2>&1; then
    killall gnome-calculator
else
    hyprctl dispatch exec gnome-calculator
fi
