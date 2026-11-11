#!/usr/bin/env bash
# Screen Recording script using wf-recorder and slurp

SAVE_DIR="$HOME/Videos/Recordings"
mkdir -p "$SAVE_DIR"

if pgrep -x wf-recorder > /dev/null; then
    pkill -INT -x wf-recorder
    pkill -RTMIN+8 waybar 2>/dev/null || true
    notify-send -a "Screen Recorder" -i "media-playback-stop" "Recording Stopped" "Video saved to $SAVE_DIR"
    exit 0
fi

GEOM=$(slurp) || exit 0
FILE="$SAVE_DIR/recording_$(date +%Y-%m-%d_%H-%M-%S).mp4"

notify-send -a "Screen Recorder" -i "media-record" "Recording Started" "Click the red REC pill in the top bar or press Super+Shift+R to stop"
pkill -RTMIN+8 waybar 2>/dev/null || true
wf-recorder -g "$GEOM" -f "$FILE"
pkill -RTMIN+8 waybar 2>/dev/null || true
