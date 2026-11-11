# 🌌 Poorya's Hyprland Desktop Setup (Catppuccin Mocha)

<p align="center">
  <img src="https://img.shields.io/badge/Compositor-Hyprland-blue?style=for-the-badge&logo=hyprland&logoColor=white" alt="Hyprland" />
  <img src="https://img.shields.io/badge/Theme-Catppuccin%20Mocha-cba6f7?style=for-the-badge" alt="Catppuccin Mocha" />
  <img src="https://img.shields.io/badge/OS-Ubuntu%20Linux-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge" alt="Status" />
</p>

A modern, fluid, battery-efficient, and pixel-perfect **Hyprland** desktop environment configured for Linux / Ubuntu. Featuring the soothing **Catppuccin Mocha** palette, custom glassmorphism widgets, dual-monitor workflow optimization, and high-productivity keybindings.

---

## 💡 About The Setup

This repository contains my personal, battle-tested dotfiles for **Hyprland** (Wayland compositor) running on **Ubuntu 26.04 LTS**. Designed from the ground up to achieve an effortless balance between aesthetic minimalism and high-speed developer productivity, this setup offers:

- **Aesthetic Consistency:** Unified **Catppuccin Mocha** dark theme across Hyprland borders, Waybar capsules, Wofi launcher, Kitty terminal, GTK 3/4 themes, and Hyprlock.
- **Dual-GPU Intelligence:** Clean Intel Iris Xe iGPU + NVIDIA GeForce RTX 4050 dGPU hybrid graphics execution with Aquamarine DRM auto-enumeration and zero screen tearing.
- **Multi-Display Synergy:** Tailored for dual-monitor workflows (144Hz laptop screen + external Samsung display) with dedicated workspace mapping, instant window throwing (<kbd>Super</kbd> + <kbd>O</kbd>), and directional screen focus.
- **Minimalist Glass Lock Screen:** Ultra-subtle, non-distracting glassmorphic `hyprlock` screen with clean typography, soft monochrome palette, and zero unnecessary visual clutter.
- **Integrated Productivity Suite:** Quick floating scratchpads, instant calculator, clipboard manager with search, color picker, wallpaper switcher, and desktop hardware telemetry widgets.
- **Reproducible & Safe Deployment:** Turnkey installation via `make install` or `./install.sh`, complete with timestamped backups of existing configurations.

---

## 📑 Table of Contents
- [About The Setup](#-about-the-setup)
- [Key Features](#-key-features)
- [Workspace Organization](#-workspace-organization)
- [Keyboard Shortcut Cheat Sheet](#-keyboard-shortcut-cheat-sheet)
  - [1. Applications & Window Navigation](#1-applications--window-navigation)
  - [2. Productivity Tools & Quick Widgets](#2-productivity-tools--quick-widgets)
  - [3. Multi-Monitor Workflow](#3-multi-monitor-workflow)
  - [4. Workspace Management](#4-workspace-management)
- [Installation Guide](#-installation-guide)
  - [Method 1: Makefile (Recommended)](#method-1-makefile-recommended)
  - [Method 2: Direct Install Script](#method-2-direct-install-script)
  - [Available Make Targets](#available-make-targets)
- [Dependencies](#-dependencies)
- [Directory Structure](#-directory-structure)

---

## 📸 Key Features

* **Multi-Monitor Synergy:** Native multi-monitor support (`eDP-1` laptop display + `HDMI-A-1` external Samsung display) with independent dynamic workspaces and instant window throwing between screens.
* **Smart Dynamic Waybar:**
  - Workspace buttons dynamically display live Nerd Font icons of active applications running inside them (e.g., `2 `, `3 󰖂`, `4 `, `5 󰧑`, `9 `).
  - Left capsule quick-launch bar for pinned daily essentials.
  - Multi-display top bar with full hardware monitoring (CPU, RAM, Battery, Power Profiles, Network, and Audio).
* **Live Dual-Card Desktop Widget (`desktop_widget.py`):**
  - **Card 1 (Hardware & System Telemetry):** Live digital clock, date, CPU usage & core temperature, RAM, NVIDIA RTX 4050 GPU telemetry (utilization, wattage, VRAM), SSD storage, upload/download network speed meters, battery status, now-playing media metadata, and system uptime.
  - **Card 2 (Daily Focus, Interactive Todo & Scratchpad):** Interactive daily task list with check-off completion and delete controls, paired with an auto-saving multi-line scratchpad for temporary notes, code snippets, and commands.
* **Instant Floating Calculator (<kbd>Super</kbd> + <kbd>C</kbd>):** A centered, floating calculator that toggles open and closed in a split second.
* **Instant Floating Scratchpad (<kbd>Super</kbd> + <kbd>T</kbd>):** Quick companion window allowing you to view and edit your daily checklist and scratchpad from inside any full-screen application without returning to the desktop.
* **Dropdown Terminal (<kbd>Super</kbd> + <kbd>`</kbd> or <kbd>Super</kbd> + <kbd>U</kbd>):** Quake-style dropdown scratchpad terminal for fast command execution.
* **Ultra-Minimal Glass Lock Screen (<kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd>):** Clean non-bold typography, frosted acrylic wallpaper blur, and a borderless translucent glass capsule password input.
* **Audio Sink Switcher (<kbd>Super</kbd> + <kbd>A</kbd>):** Instant visual audio toggle between laptop speakers and headphones.
* **Night Light (<kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>N</kbd>):** Warm color temperature shader for comfortable late-night coding.
* **Wallpaper Selector (<kbd>Super</kbd> + <kbd>W</kbd>):** GUI wallpaper browser with immediate multi-monitor background updates.

---

## 🖥️ Workspace Organization

Applications are mapped to dedicated workspaces to maintain a focused workflow:

| Workspace | Name / Icon | Primary Application |
| :---: | :---: | :--- |
| **1** | `󰋜 Zen` | Clean Desktop (Reserved, zero automatic windows) |
| **2** | ` Web` | Google Chrome (Browsing & Research) |
| **3** | `󰖂 Proxy` | Proxies & Network Tools (Karing, Hiddify, v2rayN) |
| **4** | ` Chat` | Telegram Desktop (Communication) |
| **5** | `󰧑 Dev` | Antigravity AI IDE (Development) |
| **9** | ` Music` | Spotify (Audio & Media) |
| **6 - 8, 10** | ` General` | Ad-hoc tasks, file management, and auxiliary windows |

---

## ⌨️ Keyboard Shortcut Cheat Sheet

> **Note:** The **Super** key refers to the **Windows** key on your keyboard (`$mainMod`).

### 1. Applications & Window Navigation
| Shortcut | Action |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>Enter</kbd> | Launch Default Terminal (**Kitty**) |
| <kbd>Super</kbd> + <kbd>Space</kbd> / <kbd>Super</kbd> + <kbd>R</kbd> | Open Application Launcher (**Wofi**) |
| <kbd>Super</kbd> + <kbd>E</kbd> | Launch Fast Minimal File Manager (**Thunar**) |
| <kbd>Super</kbd> + <kbd>N</kbd> | Dismiss / Close All Notifications (**Dunst**) |
| <kbd>Super</kbd> + <kbd>Ctrl</kbd> + <kbd>N</kbd> | Restore Previous Notification History |
| <kbd>Super</kbd> + <kbd>Ctrl</kbd> + <kbd>D</kbd> | Toggle Do Not Disturb (DND) Mode |
| <kbd>Super</kbd> + <kbd>I</kbd> | Open System Settings (**GNOME Control Center**) |
| <kbd>Super</kbd> + <kbd>Q</kbd> | Close Focused Window |
| <kbd>Super</kbd> + <kbd>F</kbd> | Toggle Window Fullscreen |
| <kbd>Super</kbd> + <kbd>G</kbd> / <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd> | Toggle Window Floating / Tiling |
| <kbd>Alt</kbd> + <kbd>Tab</kbd> | Fast Window Cycle |
| <kbd>Super</kbd> + <kbd>Tab</kbd> | Visual Window Switcher with Interactive Search |
| <kbd>Super</kbd> + <kbd>Left</kbd> / <kbd>Right</kbd> / <kbd>Up</kbd> / <kbd>Down</kbd> | Move Window Focus (Vim keys <kbd>H</kbd>/<kbd>J</kbd>/<kbd>K</kbd>/<kbd>L</kbd> supported) |
| <kbd>Super</kbd> + <kbd>Ctrl</kbd> + Arrows | Smooth Keyboard Window Resizing |
| <kbd>Super</kbd> + Left Click Drag | Move / Drag Window with Mouse |
| <kbd>Super</kbd> + Right Click Drag | Resize Window with Mouse |

### 2. Productivity Tools & Quick Widgets
| Shortcut | Action |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>C</kbd> | **Instant Floating Calculator** (Toggle Open / Close) |
| <kbd>Super</kbd> + <kbd>T</kbd> | **Instant Floating Daily Scratchpad & Todo Checklist** |
| <kbd>Super</kbd> + <kbd>`</kbd> / <kbd>Super</kbd> + <kbd>U</kbd> | **Quake-Style Dropdown Scratchpad Terminal** |
| <kbd>Super</kbd> + <kbd>V</kbd> | **Clipboard History Manager** (Search & Paste past clips) |
| <kbd>Super</kbd> + <kbd>A</kbd> | **Audio Output Switcher** (Speakers / Headphones) |
| <kbd>Super</kbd> + <kbd>W</kbd> | **Wallpaper Selector** (Browse & Apply) |
| <kbd>Super</kbd> + <kbd>B</kbd> | Toggle Live Desktop Widgets On / Off |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> | Color Picker (Click any pixel to copy HEX code) |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>N</kbd> | Toggle Night Light (Warm blue-light filter) |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd> / <kbd>Super</kbd> + <kbd>Esc</kbd> | **Lock Screen** (**Hyprlock**) |
| <kbd>Super</kbd> + <kbd>M</kbd> / <kbd>Super</kbd> + <kbd>Backspace</kbd> | Power Menu (Lock, Suspend, Reboot, Shutdown) |
| <kbd>Print</kbd> | Interactive Area Screenshot (Copied to Clipboard) |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Escape</kbd> | System Resource Monitor (**Btop**) |

### 3. Multi-Monitor Workflow
| Shortcut | Action |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>O</kbd> | **Throw Active Window to the Other Monitor** |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>←</kbd> / <kbd>→</kbd> | Move Active Window to Left / Right Monitor |
| <kbd>Super</kbd> + <kbd>Alt</kbd> + <kbd>O</kbd> | Switch Mouse Focus to the Other Monitor |
| <kbd>Super</kbd> + <kbd>Alt</kbd> + <kbd>←</kbd> / <kbd>→</kbd> | Switch Mouse Focus to Left / Right Monitor |
| <kbd>Super</kbd> + Left Click Drag | Drag window freely across monitor boundaries |

### 4. Workspace Management
| Shortcut | Action |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>1</kbd> .. <kbd>9</kbd> | Switch to Workspace 1 to 9 |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>1</kbd> .. <kbd>9</kbd> | Move Active Window to Workspace 1 to 9 |
| <kbd>Ctrl</kbd> + <kbd>Space</kbd> | Toggle Keyboard Input Language (English / Persian) |

---

## 🚀 Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/PooryaSN2000/poorya-hyprland.git
cd poorya-hyprland
```

### 2. Deploy Configurations
You can deploy using either the automated `Makefile` or the standalone installer:

#### Method 1: Makefile (Recommended)
```bash
make install
```

#### Method 2: Direct Install Script
```bash
./install.sh
```

> **Automatic Safe Backup:** The installer automatically creates a timestamped backup of your previous configs in `~/.config_backup_<timestamp>` before making any changes.

### Available Make Targets
```bash
make help      # Show all available make targets
make install   # Backup existing configs and deploy dotfiles
make reload    # Live-reload Hyprland and Waybar on running session
make backup    # Create a standalone timestamped backup of current configs
make check     # Validate Hyprland configuration syntax
make clean     # Clean python cache files and temporary buffers
```

---

## 📦 Dependencies

For full functionality on Ubuntu / Debian-based systems:

```bash
sudo apt update && sudo apt install -y \
  hyprland waybar wofi dunst hyprpaper hyprlock hypridle hyprland-qtutils \
  thunar tumbler thunar-archive-plugin pavucontrol blueman \
  grim slurp wl-clipboard cliphist playerctl libnotify-bin \
  gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1 python3-psutil \
  gnome-calculator kitty fonts-font-awesome
```

**Recommended Font:** [JetBrainsMono Nerd Font](https://www.nerdfonts.com/font-downloads) (required for all system glyphs and status icons).

---

## 📂 Directory Structure

```text
poorya-hyprland/
├── .config/
│   ├── hypr/                 # Hyprland compositor, lockscreen, wallpapers & scripts
│   │   ├── hyprland.conf     # Master compositor configuration
│   │   ├── hyprlock.conf     # Minimalist glass lockscreen configuration
│   │   ├── hyprpaper.conf    # Multi-monitor wallpaper daemon
│   │   ├── hypridle.conf     # Idle management configuration
│   │   ├── scripts/          # Custom helper scripts (widgets, switcher, audio, etc.)
│   │   └── wallpapers/       # High-resolution curated wallpapers
│   ├── waybar/               # Dynamic status bar (capsules, app rewrite, styling)
│   ├── wofi/                 # Application launcher styling and config
│   ├── dunst/                # Notification daemon styling (Catppuccin Mocha)
│   ├── gtk-3.0/ & gtk-4.0/   # GTK theme and color styling
│   └── xdg-desktop-portal/   # Instant-boot portal routing configurations
├── install.sh                # Executable deployment script with backup support
├── Makefile                  # Build and deployment automation
└── README.md                 # Project documentation
```

---

<p align="center">
  <i>Crafted with precision by PooryaSN.</i>
</p>
