#!/usr/bin/env bash

WALL_DIR="$HOME/.config/hypr/wallpapers"

if [ ! -d "$WALL_DIR" ]; then
    exit 1
fi

selected=$(ls "$WALL_DIR" | wofi --dmenu \
    --conf /home/pooryasn/.config/wofi/config \
    --style /home/pooryasn/.config/wofi/style.css \
    --prompt "Select Wallpaper..." \
    --width 420 \
    --height 340 \
    --hide-scroll)

if [ -n "$selected" ] && [ -f "$WALL_DIR/$selected" ]; then
    cat << EOF > "$HOME/.config/hypr/hyprpaper.conf"
wallpaper {
    monitor = eDP-1
    path = $WALL_DIR/$selected
    fit_mode = cover
}

wallpaper {
    monitor = HDMI-A-1
    path = $WALL_DIR/$selected
    fit_mode = cover
}

wallpaper {
    monitor = 
    path = $WALL_DIR/$selected
    fit_mode = cover
}

splash = false
EOF
    killall hyprpaper 2>/dev/null || true
    hyprctl dispatch exec hyprpaper
    sed -i "s|path = .*|path = $WALL_DIR/$selected|" "$HOME/.config/hypr/hyprlock.conf"
    notify-send -i "$WALL_DIR/$selected" "Wallpaper Changed" "Applied $selected to all monitors"
fi
