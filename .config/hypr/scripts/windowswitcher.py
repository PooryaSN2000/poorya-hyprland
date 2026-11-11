#!/usr/bin/env python3
"""
Window Switcher for Hyprland using Wofi
"""
import json
import subprocess
import sys

def main():
    try:
        raw = subprocess.check_output(["hyprctl", "clients", "-j"], text=True)
        clients = json.loads(raw)
    except Exception as e:
        sys.exit(1)

    # Filter out unmapped / special windows
    windows = []
    for c in clients:
        if not c.get("mapped", False):
            continue
        ws_id = c.get("workspace", {}).get("id", 0)
        ws_name = c.get("workspace", {}).get("name", str(ws_id))
        title = c.get("title", "").strip() or "Untitled"
        app_class = c.get("class", "").strip() or "App"
        addr = c.get("address", "")
        if not addr:
            continue
        
        # Friendly format: [Workspace] Title  (Class)
        label = f"[W{ws_name}] {title}  ({app_class})"
        windows.append((label, addr))

    if not windows:
        subprocess.run(["notify-send", "-a", "Hyprland", "Window Switcher", "No active windows found."])
        return

    # Pass to Wofi dmenu
    menu_input = "\n".join(item[0] for item in windows)
    try:
        proc = subprocess.Popen(
            ["wofi", "--conf", "/home/pooryasn/.config/wofi/config", "--style", "/home/pooryasn/.config/wofi/style.css", "--dmenu", "-i", "-p", "Switch to window...", "--width", "680", "--lines", str(min(12, max(4, len(windows))))],
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

    # Find address
    target_addr = None
    for label, addr in windows:
        if label == selected:
            target_addr = addr
            break

    if target_addr:
        subprocess.run(["hyprctl", "dispatch", "focuswindow", f"address:{target_addr}"])

if __name__ == "__main__":
    main()
