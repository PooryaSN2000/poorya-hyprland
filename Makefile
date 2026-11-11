.PHONY: all install backup reload check clean help

SHELL := /bin/bash
TARGET_DIR := $(HOME)/.config
BACKUP_DIR := $(HOME)/.config_backup_$(shell date +%Y%m%d_%H%M%S)

all: install

help:
	@echo "=========================================================="
	@echo "  Poorya's Hyprland Dotfiles (Catppuccin Mocha Aesthetic)  "
	@echo "=========================================================="
	@echo ""
	@echo "Usage:"
	@echo "  make install   - Backup existing configs and install dotfiles to ~/.config"
	@echo "  make backup    - Create a timestamped backup of current ~/.config files"
	@echo "  make reload    - Reload Hyprland and Waybar on running session"
	@echo "  make check     - Validate Hyprland configuration syntax"
	@echo "  make clean     - Clean python caches and temporary files"
	@echo ""

backup:
	@echo "==> Creating backup in $(BACKUP_DIR)..."
	@mkdir -p $(BACKUP_DIR)
	@for dir in hypr waybar wofi dunst gtk-3.0 gtk-4.0 xdg-desktop-portal; do \
		if [ -d "$(TARGET_DIR)/$$dir" ]; then \
			cp -r "$(TARGET_DIR)/$$dir" "$(BACKUP_DIR)/" && echo "    Backed up $$dir"; \
		fi \
	done
	@echo "==> Backup finished successfully."

install: backup
	@echo "==> Deploying configuration files to $(TARGET_DIR)..."
	@mkdir -p $(TARGET_DIR)
	@cp -r .config/* $(TARGET_DIR)/
	@echo "==> Setting executable permissions on scripts..."
	@chmod +x $(TARGET_DIR)/hypr/scripts/*
	@echo "==> Verifying Hyprland config syntax..."
	@if command -v Hyprland >/dev/null 2>&1; then \
		Hyprland --verify-config; \
	fi
	@echo ""
	@echo "=========================================================="
	@echo "  Installation Successful! Run 'make reload' to apply.    "
	@echo "=========================================================="

reload:
	@echo "==> Reloading Hyprland and Waybar..."
	@command -v hyprctl >/dev/null 2>&1 && hyprctl reload || true
	@command -v killall >/dev/null 2>&1 && killall -SIGUSR2 waybar 2>/dev/null || true
	@echo "==> Done."

check:
	@Hyprland --verify-config

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.bak" -delete 2>/dev/null || true
	@find . -name "*.swp" -delete 2>/dev/null || true
	@echo "==> Cleaned temporary files."
