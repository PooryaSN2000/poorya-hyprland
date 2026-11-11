#!/usr/bin/env python3
"""
Catppuccin Mocha Live Desktop Widget for Hyprland
Dual-card layout:
Card 1: System Info & Live Hardware Stats (Clock, CPU, RAM, GPU RTX 4050, SSD, Network, Battery, Media, Uptime)
Card 2: Daily Focus, Quick Todo Checklist & Auto-saved Scratchpad
Binds strictly to laptop primary monitor (eDP-1) on the desktop wallpaper layer.
"""
import os
import sys
import time
import json
import subprocess
import datetime
import psutil
import cairo

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, GLib, Gdk, Pango

DATA_FILE = os.path.expanduser("~/.config/hypr/scratchpad_data.json")

CSS = """
* {
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-weight: 600;
}

window,
window.widget-window,
.widget-window {
    background: transparent;
    background-color: transparent;
    border: none;
    box-shadow: none;
}

.widget-card {
    background-color: rgba(24, 24, 37, 0.88);
    border: 1.5px solid rgba(203, 166, 247, 0.35);
    border-radius: 24px;
    padding: 20px 22px;
    margin: 4px;
    box-shadow: none;
}

/* Card 1: Clock & System Stats */
.clock-time {
    font-size: 32px;
    font-weight: 800;
    color: #cba6f7;
    margin-bottom: 2px;
}

.clock-date {
    font-size: 13px;
    font-weight: 600;
    color: #89b4fa;
    margin-bottom: 4px;
}

.user-greeting {
    font-size: 12px;
    color: #a6adc8;
    margin-bottom: 10px;
}

.separator {
    background-color: #313244;
    min-height: 1px;
    margin-top: 6px;
    margin-bottom: 10px;
}

.stat-label {
    font-size: 12px;
    color: #cdd6f4;
}

.stat-value {
    font-size: 12px;
    font-weight: 700;
}

.val-cpu { color: #fab387; }
.val-ram { color: #f9e2af; }
.val-gpu { color: #a6e3a1; }
.val-disk { color: #94e2d5; }
.val-net { color: #89dceb; }
.val-bat { color: #cba6f7; }
.val-media { color: #f5c2e7; }
.val-up { color: #b4befe; }

levelbar trough {
    background-color: #313244;
    border-radius: 4px;
    min-height: 6px;
}

levelbar block.filled {
    border-radius: 4px;
}

.bar-cpu block.filled { background-color: #fab387; }
.bar-ram block.filled { background-color: #f9e2af; }
.bar-gpu block.filled { background-color: #a6e3a1; }
.bar-disk block.filled { background-color: #94e2d5; }

/* Card 2: Daily Focus, Todo & Scratchpad */
.card-title {
    font-size: 15px;
    font-weight: 800;
    color: #cba6f7;
}

.card-subtitle {
    font-size: 11px;
    color: #a6adc8;
}

.section-title {
    font-size: 12px;
    font-weight: 700;
    color: #89b4fa;
    margin-bottom: 4px;
}

.section-badge {
    font-size: 10px;
    color: #6c7086;
}

checkbutton {
    color: #cdd6f4;
    font-size: 11px;
    padding: 2px 0;
}

checkbutton check {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    min-width: 14px;
    min-height: 14px;
    margin-right: 6px;
}

checkbutton check:checked {
    background-color: #a6e3a1;
    border-color: #a6e3a1;
    color: #11111b;
}

.todo-done {
    color: #6c7086;
    text-decoration: line-through;
}

.btn-del {
    color: #6c7086;
    background: transparent;
    border: none;
    box-shadow: none;
    border-radius: 6px;
    padding: 2px 6px;
    font-size: 11px;
}

.btn-del:hover {
    color: #f38ba8;
    background-color: rgba(243, 139, 168, 0.2);
}

.todo-entry {
    background-color: rgba(49, 50, 68, 0.65);
    border: 1px solid rgba(69, 71, 90, 0.8);
    border-radius: 8px;
    color: #cdd6f4;
    padding: 5px 8px;
    font-size: 11px;
}

.todo-entry:focus {
    border-color: #cba6f7;
    background-color: rgba(49, 50, 68, 0.9);
}

.todo-add-btn {
    background-color: rgba(203, 166, 247, 0.2);
    border: 1px solid rgba(203, 166, 247, 0.4);
    border-radius: 8px;
    color: #cba6f7;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
}

.todo-add-btn:hover {
    background-color: #cba6f7;
    color: #11111b;
}

.scratchpad-view {
    background-color: rgba(30, 30, 46, 0.65);
    border: 1px solid rgba(49, 50, 68, 0.8);
    border-radius: 12px;
    color: #cdd6f4;
    padding: 8px;
    font-size: 11px;
}

.scratchpad-view:focus {
    border-color: #89b4fa;
}

scrollbar slider {
    background-color: rgba(108, 112, 134, 0.5);
    border-radius: 4px;
    min-width: 4px;
    min-height: 4px;
}

scrollbar slider:hover {
    background-color: #cba6f7;
}
"""

class DesktopWidget(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("DesktopWidget")
        self.set_name("DesktopWidget")
        self.get_style_context().add_class("widget-window")

        # RGBA visual for anti-aliased true transparency
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        self.connect("draw", self.on_draw)

        # 1. Initialize Layer Shell
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BOTTOM)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 65)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, 35)
        GtkLayerShell.set_exclusive_zone(self, 0)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.ON_DEMAND)

        # 2. Bind STRICTLY to Laptop Primary Display (eDP-1)
        self.bind_to_laptop_monitor()

        # Network speed tracking
        self.prev_net = psutil.net_io_counters()
        self.prev_time = time.time()

        # Todo & Scratchpad state
        self.data = {"todos": [], "scratchpad": ""}
        self.save_timeout_id = None
        self.last_mtime = 0
        self.load_data()

        # Build UI
        self.build_ui()
        self.apply_css()

        # Update Timers
        self.update_clock()
        self.update_fast_stats()
        self.update_slow_stats()

        GLib.timeout_add(1000, self.update_clock)
        GLib.timeout_add(2000, self.update_fast_stats)
        GLib.timeout_add(4000, self.update_slow_stats)
        GLib.timeout_add(2000, self.check_external_data_change)

    def bind_to_laptop_monitor(self):
        display = Gdk.Display.get_default()
        if not display:
            return

        target_monitor = None
        for i in range(display.get_n_monitors()):
            mon = display.get_monitor(i)
            geom = mon.get_geometry()
            # Laptop internal display is at x=1920 or model 0x0AE3
            if mon.get_model() == "0x0AE3" or geom.x == 1920:
                target_monitor = mon
                break

        if target_monitor:
            GtkLayerShell.set_monitor(self, target_monitor)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                self.last_mtime = os.path.getmtime(DATA_FILE)
            except Exception as e:
                print("Error loading data:", e)
        else:
            self.data = {
                "todos": [
                    {"text": "Thesis experiments & benchmarks", "done": False},
                    {"text": "Custom Hyprland & Waybar setup", "done": True},
                    {"text": "Review research notes & todos", "done": false}
                ],
                "scratchpad": "• Quick scratchpad for notes, commands, or thoughts.\n• Auto-saved continuously to disk."
            }
            self.save_data_immediate()

    def save_data_immediate(self):
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            self.last_mtime = os.path.getmtime(DATA_FILE)
        except Exception as e:
            print("Error saving data:", e)

    def schedule_save(self):
        if self.save_timeout_id:
            GLib.source_remove(self.save_timeout_id)
        self.save_timeout_id = GLib.timeout_add(500, self._do_save)

    def _do_save(self):
        self.save_data_immediate()
        self.save_timeout_id = None
        return False

    def check_external_data_change(self):
        if os.path.exists(DATA_FILE):
            try:
                mtime = os.path.getmtime(DATA_FILE)
                if mtime > self.last_mtime + 0.1:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        self.data = json.load(f)
                    self.last_mtime = mtime
                    self.render_todos()
                    buf = self.txt_scratch.get_buffer()
                    if buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True) != self.data.get("scratchpad", ""):
                        buf.set_text(self.data.get("scratchpad", ""))
            except Exception:
                pass
        return True

    def build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)

        # Card 1: System Info & Hardware Stats
        card_stats = self.build_stats_card()
        # Card 2: Daily Focus, Quick Todo & Scratchpad
        card_todo = self.build_todo_card()

        main_box.pack_start(card_stats, False, False, 0)
        main_box.pack_start(card_todo, False, False, 0)

        self.add(main_box)

    def build_stats_card(self):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        card.get_style_context().add_class("widget-card")
        card.set_size_request(310, -1)

        # Clock & Date Header
        self.lbl_time = Gtk.Label(xalign=0)
        self.lbl_time.get_style_context().add_class("clock-time")

        self.lbl_date = Gtk.Label(xalign=0)
        self.lbl_date.get_style_context().add_class("clock-date")

        user = os.environ.get("USER", "pooryasn")
        self.lbl_greeting = Gtk.Label(label=f"󰄛 Welcome back, {user}", xalign=0)
        self.lbl_greeting.get_style_context().add_class("user-greeting")

        sep1 = Gtk.Box()
        sep1.get_style_context().add_class("separator")

        card.pack_start(self.lbl_time, False, False, 0)
        card.pack_start(self.lbl_date, False, False, 0)
        card.pack_start(self.lbl_greeting, False, False, 0)
        card.pack_start(sep1, False, False, 0)

        # 1. CPU Row (Usage + Temp)
        self.lbl_cpu, self.bar_cpu, box_cpu = self.create_stat_row("󰍛 CPU", "val-cpu", "bar-cpu")
        card.pack_start(box_cpu, False, False, 3)

        # 2. RAM Row
        self.lbl_ram, self.bar_ram, box_ram = self.create_stat_row("󰘚 RAM", "val-ram", "bar-ram")
        card.pack_start(box_ram, False, False, 3)

        # 3. GPU Row (NVIDIA RTX 4050)
        self.lbl_gpu, self.bar_gpu, box_gpu = self.create_stat_row("󰢮 GPU (RTX 4050)", "val-gpu", "bar-gpu")
        card.pack_start(box_gpu, False, False, 3)

        # 4. Storage Row (Disk)
        self.lbl_disk, self.bar_disk, box_disk = self.create_stat_row("󰋊 Disk", "val-disk", "bar-disk")
        card.pack_start(box_disk, False, False, 3)

        sep2 = Gtk.Box()
        sep2.get_style_context().add_class("separator")
        card.pack_start(sep2, False, False, 0)

        # 5. Network Speed
        self.lbl_net = Gtk.Label(xalign=0)
        self.lbl_net.get_style_context().add_class("stat-value")
        self.lbl_net.get_style_context().add_class("val-net")
        card.pack_start(self.lbl_net, False, False, 2)

        # 6. Battery Status
        self.lbl_bat = Gtk.Label(xalign=0)
        self.lbl_bat.get_style_context().add_class("stat-value")
        self.lbl_bat.get_style_context().add_class("val-bat")
        card.pack_start(self.lbl_bat, False, False, 2)

        # 7. Media Player / Now Playing
        self.lbl_media = Gtk.Label(xalign=0)
        self.lbl_media.get_style_context().add_class("stat-value")
        self.lbl_media.get_style_context().add_class("val-media")
        card.pack_start(self.lbl_media, False, False, 2)

        # 8. System Uptime
        self.lbl_up = Gtk.Label(xalign=0)
        self.lbl_up.get_style_context().add_class("stat-value")
        self.lbl_up.get_style_context().add_class("val-up")
        card.pack_start(self.lbl_up, False, False, 2)

        return card

    def build_todo_card(self):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        card.get_style_context().add_class("widget-card")
        card.set_size_request(330, -1)

        # Header: Title & Counter
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_title = Gtk.Label(label="󰃭 Daily Focus", xalign=0)
        lbl_title.get_style_context().add_class("card-title")

        self.lbl_todo_counter = Gtk.Label(xalign=1)
        self.lbl_todo_counter.get_style_context().add_class("card-subtitle")

        header_box.pack_start(lbl_title, True, True, 0)
        header_box.pack_end(self.lbl_todo_counter, False, False, 0)
        card.pack_start(header_box, False, False, 0)

        sep1 = Gtk.Box()
        sep1.get_style_context().add_class("separator")
        card.pack_start(sep1, False, False, 0)

        # Scrollable Todo Items Box
        self.todo_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        scrolled_todo = Gtk.ScrolledWindow()
        scrolled_todo.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_todo.set_size_request(-1, 130)
        scrolled_todo.add(self.todo_list_box)
        card.pack_start(scrolled_todo, False, False, 0)

        # Add Task Row (Entry + Add Button)
        add_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        add_box.set_margin_top(6)
        add_box.set_margin_bottom(6)

        self.entry_todo = Gtk.Entry()
        self.entry_todo.set_placeholder_text("Add task... (Press Enter)")
        self.entry_todo.get_style_context().add_class("todo-entry")
        self.entry_todo.connect("activate", self.on_add_task)

        btn_add = Gtk.Button(label="󰐕 Add")
        btn_add.get_style_context().add_class("todo-add-btn")
        btn_add.connect("clicked", self.on_add_task)

        add_box.pack_start(self.entry_todo, True, True, 0)
        add_box.pack_end(btn_add, False, False, 0)
        card.pack_start(add_box, False, False, 0)

        sep2 = Gtk.Box()
        sep2.get_style_context().add_class("separator")
        card.pack_start(sep2, False, False, 0)

        # Scratchpad Header
        scratch_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_scratch_title = Gtk.Label(label="󰠮 Quick Scratchpad", xalign=0)
        lbl_scratch_title.get_style_context().add_class("section-title")

        lbl_scratch_badge = Gtk.Label(label="(Auto-saved)", xalign=1)
        lbl_scratch_badge.get_style_context().add_class("section-badge")

        scratch_header.pack_start(lbl_scratch_title, True, True, 0)
        scratch_header.pack_end(lbl_scratch_badge, False, False, 0)
        card.pack_start(scratch_header, False, False, 2)

        # Scratchpad Text Area
        scrolled_text = Gtk.ScrolledWindow()
        scrolled_text.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_text.set_size_request(-1, 105)

        self.txt_scratch = Gtk.TextView()
        self.txt_scratch.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.txt_scratch.get_style_context().add_class("scratchpad-view")
        buf = self.txt_scratch.get_buffer()
        buf.set_text(self.data.get("scratchpad", ""))
        buf.connect("changed", self.on_scratchpad_changed)

        scrolled_text.add(self.txt_scratch)
        card.pack_start(scrolled_text, True, True, 0)

        # Initial render of todos
        self.render_todos()

        return card

    def render_todos(self):
        # Clear existing
        for child in self.todo_list_box.get_children():
            self.todo_list_box.remove(child)

        todos = self.data.get("todos", [])
        completed = sum(1 for t in todos if t.get("done", False))
        total = len(todos)
        self.lbl_todo_counter.set_text(f"{completed}/{total} done")

        for idx, item in enumerate(todos):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

            chk = Gtk.CheckButton(label=item.get("text", ""))
            chk.set_active(item.get("done", False))
            if item.get("done", False):
                chk.get_style_context().add_class("todo-done")
            chk.connect("toggled", self.on_toggle_task, idx)

            btn_del = Gtk.Button(label="󰅖")
            btn_del.set_tooltip_text("Delete task")
            btn_del.get_style_context().add_class("btn-del")
            btn_del.connect("clicked", self.on_delete_task, idx)

            row.pack_start(chk, True, True, 0)
            row.pack_end(btn_del, False, False, 0)
            self.todo_list_box.pack_start(row, False, False, 1)

        self.todo_list_box.show_all()

    def on_add_task(self, widget):
        text = self.entry_todo.get_text().strip()
        if text:
            if "todos" not in self.data:
                self.data["todos"] = []
            self.data["todos"].append({"text": text, "done": False})
            self.entry_todo.set_text("")
            self.render_todos()
            self.schedule_save()

    def on_toggle_task(self, widget, idx):
        todos = self.data.get("todos", [])
        if 0 <= idx < len(todos):
            todos[idx]["done"] = widget.get_active()
            self.render_todos()
            self.schedule_save()

    def on_delete_task(self, widget, idx):
        todos = self.data.get("todos", [])
        if 0 <= idx < len(todos):
            todos.pop(idx)
            self.render_todos()
            self.schedule_save()

    def on_scratchpad_changed(self, buf):
        start = buf.get_start_iter()
        end = buf.get_end_iter()
        self.data["scratchpad"] = buf.get_text(start, end, True)
        self.schedule_save()

    def create_stat_row(self, title, val_class, bar_class):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_title = Gtk.Label(label=title, xalign=0)
        lbl_title.get_style_context().add_class("stat-label")

        lbl_val = Gtk.Label(label="--%", xalign=1)
        lbl_val.get_style_context().add_class("stat-value")
        lbl_val.get_style_context().add_class(val_class)

        hbox.pack_start(lbl_title, True, True, 0)
        hbox.pack_end(lbl_val, False, False, 0)

        bar = Gtk.LevelBar()
        bar.set_min_value(0.0)
        bar.set_max_value(100.0)
        bar.set_value(0.0)
        bar.get_style_context().add_class(bar_class)

        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(bar, False, False, 0)

        return lbl_val, bar, vbox

    def update_clock(self):
        now = datetime.datetime.now()
        self.lbl_time.set_text(now.strftime("%H:%M:%S"))
        self.lbl_date.set_text(now.strftime("󰸗 %A, %d %B %Y"))
        return True

    def update_fast_stats(self):
        # 1. CPU Usage & Temp
        cpu = psutil.cpu_percent()
        cpu_temp_str = ""
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps and temps['coretemp']:
                cur = int(temps['coretemp'][0].current)
                cpu_temp_str = f" ({cur}°C)"
        except Exception:
            pass

        self.lbl_cpu.set_text(f"{cpu:0.1f}%{cpu_temp_str}")
        self.bar_cpu.set_value(cpu)

        # 2. RAM Usage
        mem = psutil.virtual_memory()
        self.lbl_ram.set_text(f"{mem.percent:0.1f}% ({mem.used/(1024**3):0.1f}/{mem.total/(1024**3):0.1f}GB)")
        self.bar_ram.set_value(mem.percent)

        # 3. Network Speed
        now = time.time()
        dt = max(1.0, now - self.prev_time)
        net = psutil.net_io_counters()
        down_bps = (net.bytes_recv - self.prev_net.bytes_recv) / dt
        up_bps = (net.bytes_sent - self.prev_net.bytes_sent) / dt
        self.prev_net = net
        self.prev_time = now

        def fmt_speed(b):
            if b >= 1024 * 1024:
                return f"{b/(1024*1024):0.1f} MB/s"
            elif b >= 1024:
                return f"{b/1024:0.0f} KB/s"
            return f"{b:0.0f} B/s"

        self.lbl_net.set_text(f"󰤨 Net   󰁅 {fmt_speed(down_bps)}  󰁝 {fmt_speed(up_bps)}")

        # 4. Media Player (playerctl)
        try:
            status = subprocess.check_output(
                ["playerctl", "status"], text=True, stderr=subprocess.DEVNULL
            ).strip()
            if status:
                title = subprocess.check_output(
                    ["playerctl", "metadata", "--format", "{{ artist }} - {{ title }}"],
                    text=True, stderr=subprocess.DEVNULL
                ).strip()
                if not title:
                    title = "Playing Media"
                if len(title) > 28:
                    title = title[:26] + "…"
                icon = "󰎆" if status == "Playing" else "󰏤"
                self.lbl_media.set_text(f"{icon} Media {title}")
            else:
                self.lbl_media.set_text("󰎆 Media Idle")
        except Exception:
            self.lbl_media.set_text("󰎆 Media Idle")

        return True

    def update_slow_stats(self):
        # 1. GPU (NVIDIA RTX 4050)
        try:
            smi = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,power.draw,memory.used,memory.total", "--format=csv,noheader,nounits"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            parts = [p.strip() for p in smi.split(",")]
            if len(parts) >= 5:
                temp = int(parts[0])
                util = int(parts[1])
                power = float(parts[2])
                vram_used = int(parts[3])
                vram_tot = int(parts[4])
                self.lbl_gpu.set_text(f"{util}% ({temp}°C • {int(round(power))}W)")
                self.lbl_gpu.set_tooltip_text(
                    f"NVIDIA GeForce RTX 4050 Laptop GPU\n"
                    f"Power Draw: {power:.1f}W / 80W (Downclocked Power-Save State)\n"
                    f"VRAM Used: {vram_used} MB / {vram_tot} MB\n"
                    f"Driving: HDMI-A-1 (External Display @ 60Hz)"
                )
                self.bar_gpu.set_value(util)
            else:
                self.lbl_gpu.set_text("Active")
                self.bar_gpu.set_value(10)
        except Exception:
            self.lbl_gpu.set_text("Intel iGPU")
            self.bar_gpu.set_value(0)

        # 2. Disk
        disk = psutil.disk_usage('/')
        self.lbl_disk.set_text(f"{disk.percent:0.1f}% ({disk.free/(1024**3):0.1f}GB free)")
        self.bar_disk.set_value(disk.percent)

        # 3. Battery
        try:
            battery = psutil.sensors_battery()
            if battery:
                icon = "󰂄" if battery.power_plugged else "󰁹"
                status = "Plugged" if battery.power_plugged else "Battery"
                self.lbl_bat.set_text(f"{icon} Bat   {battery.percent:0.0f}% ({status})")
            else:
                self.lbl_bat.set_text("󰚥 AC Connected")
        except Exception:
            self.lbl_bat.set_text("󰚥 AC Power")

        # 4. Uptime
        try:
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot_time
            hours, remainder = divmod(int(uptime.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            self.lbl_up.set_text(f"󰔛 Up    {hours}h {minutes}m")
        except Exception:
            self.lbl_up.set_text("󰔛 Up    Active")

        return True

    def apply_css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        return False

def main():
    Gtk.init(None)
    win = DesktopWidget()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
