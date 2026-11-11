#!/usr/bin/env python3
"""
Floating Daily Scratchpad & Quick Todo Window for Hyprland
Toggled with Super + T anywhere in any workspace.
Shares and synchronizes state with ~/.config/hypr/scratchpad_data.json
"""
import os
import sys
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

DATA_FILE = os.path.expanduser("~/.config/hypr/scratchpad_data.json")

CSS = """
* {
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-weight: 600;
}

window {
    background-color: #181825;
    color: #cdd6f4;
}

.window-card {
    padding: 18px 20px;
    background-color: #181825;
}

.card-title {
    font-size: 16px;
    font-weight: 800;
    color: #cba6f7;
}

.card-subtitle {
    font-size: 11px;
    color: #a6adc8;
}

.separator {
    background-color: #313244;
    min-height: 1px;
    margin-top: 8px;
    margin-bottom: 12px;
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
    background-color: rgba(49, 50, 68, 0.7);
    border: 1px solid rgba(69, 71, 90, 0.8);
    border-radius: 8px;
    color: #cdd6f4;
    padding: 6px 10px;
    font-size: 11px;
}

.todo-entry:focus {
    border-color: #cba6f7;
    background-color: rgba(49, 50, 68, 0.95);
}

.todo-add-btn {
    background-color: rgba(203, 166, 247, 0.2);
    border: 1px solid rgba(203, 166, 247, 0.4);
    border-radius: 8px;
    color: #cba6f7;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
}

.todo-add-btn:hover {
    background-color: #cba6f7;
    color: #11111b;
}

.scratchpad-view {
    background-color: rgba(30, 30, 46, 0.8);
    border: 1px solid rgba(49, 50, 68, 0.8);
    border-radius: 12px;
    color: #cdd6f4;
    padding: 10px;
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

class ScratchpadWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Daily Scratchpad & Quick Todo")
        self.set_default_size(420, 560)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.data = {"todos": [], "scratchpad": ""}
        self.save_timeout_id = None
        self.load_data()

        self.build_ui()
        self.apply_css()

        self.connect("key-press-event", self.on_key_press)

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.save_immediate()
            Gtk.main_quit()
            return True
        return False

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print("Error loading:", e)

    def save_immediate(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Error saving:", e)

    def schedule_save(self):
        if self.save_timeout_id:
            GLib.source_remove(self.save_timeout_id)
        self.save_timeout_id = GLib.timeout_add(400, self._do_save)

    def _do_save(self):
        self.save_immediate()
        self.save_timeout_id = None
        return False

    def build_ui(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.get_style_context().add_class("window-card")

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_title = Gtk.Label(label="󰃭 Daily Focus & Tasks", xalign=0)
        lbl_title.get_style_context().add_class("card-title")

        self.lbl_counter = Gtk.Label(xalign=1)
        self.lbl_counter.get_style_context().add_class("card-subtitle")

        header.pack_start(lbl_title, True, True, 0)
        header.pack_end(self.lbl_counter, False, False, 0)
        box.pack_start(header, False, False, 0)

        sep1 = Gtk.Box()
        sep1.get_style_context().add_class("separator")
        box.pack_start(sep1, False, False, 0)

        # Scrolled Todo List
        self.todo_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(-1, 170)
        scrolled.add(self.todo_list_box)
        box.pack_start(scrolled, True, True, 0)

        # Add Entry Row
        add_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        add_box.set_margin_top(8)
        add_box.set_margin_bottom(8)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Add new task... (Press Enter)")
        self.entry.get_style_context().add_class("todo-entry")
        self.entry.connect("activate", self.on_add_task)

        btn_add = Gtk.Button(label="󰐕 Add")
        btn_add.get_style_context().add_class("todo-add-btn")
        btn_add.connect("clicked", self.on_add_task)

        add_box.pack_start(self.entry, True, True, 0)
        add_box.pack_end(btn_add, False, False, 0)
        box.pack_start(add_box, False, False, 0)

        sep2 = Gtk.Box()
        sep2.get_style_context().add_class("separator")
        box.pack_start(sep2, False, False, 0)

        # Scratchpad Header
        scratch_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_scratch_title = Gtk.Label(label="󰠮 Quick Scratchpad", xalign=0)
        lbl_scratch_title.get_style_context().add_class("section-title")

        lbl_badge = Gtk.Label(label="(Auto-saved)", xalign=1)
        lbl_badge.get_style_context().add_class("section-badge")

        scratch_header.pack_start(lbl_scratch_title, True, True, 0)
        scratch_header.pack_end(lbl_badge, False, False, 0)
        box.pack_start(scratch_header, False, False, 2)

        # Scratchpad View
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.set_size_request(-1, 140)

        self.tv = Gtk.TextView()
        self.tv.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.tv.get_style_context().add_class("scratchpad-view")
        buf = self.tv.get_buffer()
        buf.set_text(self.data.get("scratchpad", ""))
        buf.connect("changed", self.on_scratch_changed)

        sw.add(self.tv)
        box.pack_start(sw, True, True, 0)

        self.add(box)
        self.render_todos()

    def render_todos(self):
        for child in self.todo_list_box.get_children():
            self.todo_list_box.remove(child)

        todos = self.data.get("todos", [])
        done_cnt = sum(1 for t in todos if t.get("done", False))
        self.lbl_counter.set_text(f"{done_cnt}/{len(todos)} done")

        for idx, item in enumerate(todos):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

            chk = Gtk.CheckButton(label=item.get("text", ""))
            chk.set_active(item.get("done", False))
            if item.get("done", False):
                chk.get_style_context().add_class("todo-done")
            chk.connect("toggled", self.on_toggle, idx)

            btn_del = Gtk.Button(label="󰅖")
            btn_del.get_style_context().add_class("btn-del")
            btn_del.connect("clicked", self.on_delete, idx)

            row.pack_start(chk, True, True, 0)
            row.pack_end(btn_del, False, False, 0)
            self.todo_list_box.pack_start(row, False, False, 1)

        self.todo_list_box.show_all()

    def on_add_task(self, widget):
        t = self.entry.get_text().strip()
        if t:
            if "todos" not in self.data:
                self.data["todos"] = []
            self.data["todos"].append({"text": t, "done": False})
            self.entry.set_text("")
            self.render_todos()
            self.schedule_save()

    def on_toggle(self, widget, idx):
        todos = self.data.get("todos", [])
        if 0 <= idx < len(todos):
            todos[idx]["done"] = widget.get_active()
            self.render_todos()
            self.schedule_save()

    def on_delete(self, widget, idx):
        todos = self.data.get("todos", [])
        if 0 <= idx < len(todos):
            todos.pop(idx)
            self.render_todos()
            self.schedule_save()

    def on_scratch_changed(self, buf):
        start = buf.get_start_iter()
        end = buf.get_end_iter()
        self.data["scratchpad"] = buf.get_text(start, end, True)
        self.schedule_save()

    def apply_css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def main():
    Gtk.init(None)
    win = ScratchpadWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
