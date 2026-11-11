#!/usr/bin/env bash

selected=$(cliphist list | wofi --dmenu \
    --conf /home/pooryasn/.config/wofi/config \
    --style /home/pooryasn/.config/wofi/style.css \
    --prompt "Search Clipboard..." \
    --width 560 \
    --height 400 \
    --hide-scroll)

if [ -n "$selected" ]; then
    echo "$selected" | cliphist decode | wl-copy
    notify-send -i edit-paste "Clipboard" "Item copied back to active clipboard."
fi
