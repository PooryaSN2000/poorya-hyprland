#!/usr/bin/env python3
"""
Audio Output Switcher for PipeWire (WirePlumber) using Wofi
"""
import re
import subprocess
import sys

def main():
    try:
        out = subprocess.check_output(["wpctl", "status"], text=True)
    except Exception as e:
        sys.exit(1)

    in_sinks = False
    sinks = []
    for line in out.splitlines():
        if "Sinks:" in line:
            in_sinks = True
            continue
        if in_sinks:
            if any(k in line for k in ["Sources:", "Filters:", "Streams:", "Video", "Settings"]):
                break
            m = re.search(r"([* ]*)\s+(\d+)\.\s+(.*?)\s+\[vol:", line)
            if m:
                is_active = "*" in m.group(1)
                sink_id = m.group(2)
                name = m.group(3).strip()
                sinks.append((is_active, sink_id, name))

    if not sinks:
        subprocess.run(["notify-send", "-a", "Audio", "Audio Switcher", "No audio outputs found."])
        return

    options = []
    for is_active, sid, name in sinks:
        status_icon = "󰄴 " if is_active else "   "
        options.append(f"{status_icon} {name}")

    menu_input = "\n".join(options)
    try:
        proc = subprocess.Popen(
            ["wofi", "--conf", "/home/pooryasn/.config/wofi/config", "--style", "/home/pooryasn/.config/wofi/style.css", "--dmenu", "-i", "-p", "Select Audio Output...", "--width", "540", "--lines", str(len(options) + 1)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        selected, _ = proc.communicate(input=menu_input)
    except Exception:
        return

    selected = selected.strip()
    if not selected:
        return

    # Match selected back to sink_id
    for is_active, sid, name in sinks:
        status_icon = "󰄴 " if is_active else "   "
        line_match = f"{status_icon} {name}".strip()
        if selected == line_match or name in selected:
            subprocess.run(["wpctl", "set-default", sid])
            subprocess.run(["notify-send", "-a", "Audio", "-i", "audio-speakers", "Audio Output Changed", f"Active: {name}"])
            break

if __name__ == "__main__":
    main()
