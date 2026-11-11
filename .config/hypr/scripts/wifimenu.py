#!/usr/bin/env python3
import subprocess
import sys

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""

def notify(title, msg, icon="network-wireless"):
    subprocess.Popen(["notify-send", "-i", icon, title, msg])

def main():
    # 1. Fetch available Wi-Fi networks
    raw = run_cmd(["nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY", "device", "wifi", "list"])
    networks = {}

    for line in raw.strip().split("\n"):
        if not line:
            continue
        parts = line.split(":")
        if len(parts) >= 3:
            in_use = (parts[0].strip() == "*")
            ssid = parts[1].strip()
            if not ssid or ssid == "--":
                continue
            try:
                signal = int(parts[2].strip())
            except ValueError:
                signal = 0
            security = parts[3].strip() if len(parts) > 3 else ""

            if ssid not in networks or signal > networks[ssid]["signal"] or in_use:
                networks[ssid] = {
                    "in_use": in_use,
                    "signal": signal,
                    "security": security
                }

    lines = []
    items_map = {}

    for ssid, info in sorted(networks.items(), key=lambda x: (not x[1]["in_use"], -x[1]["signal"])):
        sig = info["signal"]
        icon_sig = "󰤨" if sig > 65 else ("󰤥" if sig > 40 else "󰤢")
        icon_lock = " 󰌾" if info["security"] else ""

        if info["in_use"]:
            display = f"󰄬  {icon_sig}  {ssid} ({sig}%){icon_lock}  [Connected]"
        else:
            display = f"    {icon_sig}  {ssid} ({sig}%){icon_lock}"

        lines.append(display)
        items_map[display] = ssid

    lines.append("")
    lines.append("󰤭  Disconnect")
    lines.append("󰑓  Rescan Networks")
    lines.append("  Network Settings")

    # 2. Show wofi modal
    menu_input = "\n".join(lines)
    p = subprocess.Popen(
        ["wofi", "--conf", "/home/pooryasn/.config/wofi/config", "--style", "/home/pooryasn/.config/wofi/style.css", "--dmenu", "--prompt", "Wi-Fi Networks", "--width", "380", "--height", "400", "--hide-scroll"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    selected, _ = p.communicate(input=menu_input)
    selected = selected.strip()

    if not selected:
        return

    if "Disconnect" in selected:
        run_cmd(["nmcli", "device", "disconnect", "wlp9s0"])
        notify("Wi-Fi", "Disconnected from network.", "network-wireless-disconnected")
        return

    if "Rescan Networks" in selected:
        notify("Wi-Fi", "Scanning for networks...")
        run_cmd(["nmcli", "device", "wifi", "rescan"])
        subprocess.Popen([sys.executable, __file__])
        return

    if "Network Settings" in selected:
        subprocess.Popen(["env", "XDG_CURRENT_DESKTOP=GNOME", "gnome-control-center", "wifi"])
        return

    ssid = items_map.get(selected)
    if not ssid:
        return

    info = networks.get(ssid, {})
    if info.get("in_use"):
        notify("Wi-Fi", f"Already connected to {ssid}.")
        return

    # Check if network is saved
    saved = run_cmd(["nmcli", "-t", "-f", "NAME", "connection", "show"])
    is_saved = ssid in [c.strip() for c in saved.split("\n")]

    if is_saved:
        notify("Wi-Fi", f"Connecting to {ssid}...")
        res = subprocess.run(["nmcli", "connection", "up", "id", ssid], capture_output=True, text=True)
        if res.returncode == 0:
            notify("Wi-Fi", f"Connected to {ssid}.")
        else:
            notify("Wi-Fi Error", f"Failed to connect to {ssid}.", "network-error")
        return

    # Open network (no password needed)
    if not info.get("security"):
        notify("Wi-Fi", f"Connecting to {ssid}...")
        res = subprocess.run(["nmcli", "device", "wifi", "connect", ssid], capture_output=True, text=True)
        if res.returncode == 0:
            notify("Wi-Fi", f"Connected to {ssid}.")
        else:
            notify("Wi-Fi Error", f"Failed to connect to {ssid}.", "network-error")
        return

    # Secured network -> Ask for password in English
    p_pass = subprocess.Popen(
        ["wofi", "--conf", "/home/pooryasn/.config/wofi/config", "--style", "/home/pooryasn/.config/wofi/style.css", "--dmenu", "--password", "--prompt", f"Password for {ssid}:", "--width", "340", "--height", "140", "--hide-scroll"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    password, _ = p_pass.communicate(input="")
    password = password.strip()

    if not password:
        return

    notify("Wi-Fi", f"Authenticating with {ssid}...")
    res = subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], capture_output=True, text=True)
    if res.returncode == 0:
        notify("Wi-Fi", f"Connected to {ssid}.")
    else:
        notify("Wi-Fi Error", "Invalid password or connection timed out.", "network-error")

if __name__ == "__main__":
    main()
