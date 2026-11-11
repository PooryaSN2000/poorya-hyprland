# 🌌 Poorya's Hyprland Desktop Setup (Catppuccin Mocha)

A modern, fluid, and battery-efficient **Hyprland** desktop environment configured for Ubuntu / Linux with the **Catppuccin Mocha** color palette, custom glassmorphism widgets, dual-monitor workflow, and seamless productivity shortcuts.

---

## 📸 Key Features

* **Dual-Monitor Optimization:** Automatic multi-monitor management (`eDP-1` laptop display + `HDMI-A-1` external monitor) with independent workspace routing.
* **Smart Dynamic Waybar:**
  - Workspace buttons automatically display live Nerd Font icons of active applications inside each workspace (e.g., `2 `, `3 󰖂`, `4 `, `5 󰧑`, `9 `).
  - Left quick-launch capsule for pinned daily apps.
  - Multi-monitor support across all active screens.
* **Dedicated Workspace Layout:**
  - `Workspace 1`: Clean Zen Desktop (no auto-launched windows)
  - `Workspace 2`: Google Chrome (Web Browsing)
  - `Workspace 3`: Proxies & Network Tools (Karing, Hiddify, v2rayN)
  - `Workspace 4`: Telegram Desktop (Communication)
  - `Workspace 5`: Antigravity AI IDE (Development)
  - `Workspace 9`: Spotify (Music)
* **Live Dual-Card Desktop Widget (`desktop_widget.py`):**
  - **Card 1 (Hardware & System):** Live Clock, CPU usage & temperature, RAM, NVIDIA RTX 4050 GPU utilization/power/VRAM, SSD storage, upload/download network speed, battery status, now-playing media, and uptime.
  - **Card 2 (Daily Focus & Quick Scratchpad):** Interactive daily todo checklist with checkbox toggle & delete, plus an auto-saving multi-line scratchpad for temporary notes and code snippets.
* **Instant Floating Calculator (`Super + C`):** Centered floating calculator that opens and closes instantly with a single keystroke.
* **Instant Floating Scratchpad (`Super + T`):** Access and edit your daily checklist and notes from inside any full-screen app without switching to the desktop.
* **Dropdown Terminal (`Super + Grave` or `Super + U`):** Quake-style dropdown scratchpad terminal.
* **Ultra-Minimal Glass Lock Screen (`Super + Shift + L`):** Clean typography, soft frosted acrylic wallpaper blur, and borderless translucent glass password field.
* **Sound Output Switcher (`Super + A`):** One-key visual audio switcher between laptop speakers and headphones.
* **Night Light (`Super + Shift + N`):** Warms display color temperature for night coding.
* **Wallpaper Selector (`Super + W`):** Visual wallpaper browser with dynamic update.

---

## ⌨️ Shortcut Cheat Sheet

 کلید اصلی **Super** همان کلید **ویندوز** روی کیبورد شماست (`$mainMod`).

### ۱. برنامه‌ها و ناوبری پنجره‌ها (Applications & Windows)
| میانبر | عملکرد |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>Enter</kbd> | باز کردن ترمینال پیش‌فرض (Ptyxis) |
| <kbd>Super</kbd> + <kbd>Space</kbd> یا <kbd>Super</kbd> + <kbd>R</kbd> | منوی لانچر برنامه‌ها (Wofi App Menu) |
| <kbd>Super</kbd> + <kbd>E</kbd> | فایل منیجر ناتیلوس (Files) |
| <kbd>Super</kbd> + <kbd>I</kbd> | تنظیمات سیستم (GNOME Settings) |
| <kbd>Super</kbd> + <kbd>Q</kbd> | بستن پنجره فعال (Close Window) |
| <kbd>Super</kbd> + <kbd>F</kbd> | تمام‌صفحه کردن پنجره (Toggle Fullscreen) |
| <kbd>Super</kbd> + <kbd>G</kbd> یا <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd> | تغییر وضعیت شناور / تایل (Toggle Floating) |
| <kbd>Alt</kbd> + <kbd>Tab</kbd> | چرخش سریع بین پنجره‌ها (Fast Window Cycle) |
| <kbd>Super</kbd> + <kbd>Tab</kbd> | سوییچر تصویری پنجره‌ها با جستجو (Visual Window Switcher) |

### ۲. ابزارهای بهره‌وری و ویجت‌ها (Productivity & Tools)
| میانبر | عملکرد |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>C</kbd> | **ماشین‌حساب شناور آنی (Instant Floating Calculator)** |
| <kbd>Super</kbd> + <kbd>T</kbd> | **یادداشت و چک‌لیست سریع شناور (Daily Scratchpad & Todo)** |
| <kbd>Super</kbd> + <kbd>`</kbd> یا <kbd>Super</kbd> + <kbd>U</kbd> | **ترمینال شناور سریع (Dropdown Scratchpad Terminal)** |
| <kbd>Super</kbd> + <kbd>V</kbd> | **تاریخچه کلیپ‌بورد (Clipboard History Manager)** |
| <kbd>Super</kbd> + <kbd>A</kbd> | **تغییر سریع خروجی صدا (اسپیکر / هدفون)** |
| <kbd>Super</kbd> + <kbd>W</kbd> | **انتخابگر گرافیکی والپیپر (Wallpaper Selector)** |
| <kbd>Super</kbd> + <kbd>B</kbd> | مخفی‌سازی / نمایش ویجت‌های دسکتاپ |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> | قطره‌چکان رنگ و کپی کد HEX (Color Picker) |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>N</kbd> | حالت محافظ چشم / نور شب (Night Light) |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd> یا <kbd>Super</kbd> + <kbd>Esc</kbd> | **قفل صفحه فوق‌مینیمال شیشه‌ای (Hyprlock)** |
| <kbd>Super</kbd> + <kbd>M</kbd> یا <kbd>Super</kbd> + <kbd>Backspace</kbd> | منوی خاموش کردن و ریبوت سیستم (Power Menu) |
| <kbd>Print</kbd> | اسکرین‌شات از ناحیه انتخابی صفحه |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Escape</kbd> | تسک منیجر و مانیتورینگ منابع سیستم |

### ۳. مدیریت صفحات (Workspaces)
| میانبر | عملکرد |
| :--- | :--- |
| <kbd>Super</kbd> + <kbd>1</kbd> تا <kbd>9</kbd> | رفتن به صفحه مربوطه |
| <kbd>Super</kbd> + <kbd>Shift</kbd> + <kbd>1</kbd> تا <kbd>9</kbd> | انتقال پنجره به صفحه مربوطه |
| <kbd>Ctrl</kbd> + <kbd>Space</kbd> | تغییر زبان کیبورد (انگلیسی / فارسی) |

---

## 🚀 روش نصب و اعمال (Installation)

### ۱. کلون کردن ریپازیتوری
```bash
git clone https://github.com/PooryaSN2000/poorya-hyprland.git
cd poorya-hyprland
```

### ۲. اعمال تنظیمات (با استفاده از Makefile یا اسکریپت)
می‌توانید به سادگی یکی از دو دستور زیر را اجرا کنید:

```bash
make install
```
یا:
```bash
./install.sh
```

> **نکته امنیتی:** اسکریپت نصب قبل از اعمال هرگونه فایل، به‌صورت خودکار یک نسخه پشتیبان از کانفیگ‌های قبلی شما در پوشه `~/.config_backup_<timestamp>` ذخیره می‌کند.

### دستورات تکمیلی Makefile:
```bash
make help      # مشاهده راهنمای دستورات موجود
make reload    # ریلود آنی Hyprland و Waybar
make backup    # تهیه نسخه پشتیبان دستی
make check     # اعتبارسنجی سینتکس کانفیگ Hyprland
make clean     # پاک‌سازی فایل‌های موقت
```

---

## 📦 پیش‌نیازها (Dependencies)

برای کارکرد ۱۰۰٪ تمام قابلیت‌ها در سیستم‌های بر پایه اوبونتو/دبیان:
```bash
sudo apt update && sudo apt install -y \
  hyprland waybar wofi dunst hyprpaper hyprlock hypridle \
  grim slurp wl-clipboard cliphist playerctl libnotify-bin \
  gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1 python3-psutil \
  gnome-calculator ptyxis fonts-font-awesome
```
فونت پیشنهادی برای تمام آیکون‌ها: **JetBrainsMono Nerd Font**.

---
*Created with ❤️ by PooryaSN.*
