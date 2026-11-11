#!/usr/bin/env bash
# Poorya's Hyprland Setup & Installation Script
# Automated deployment of configs, dependencies, and permissions

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================================${NC}"
echo -e "${BLUE}   PooryaSN Hyprland & Catppuccin Mocha Installer        ${NC}"
echo -e "${BLUE}==========================================================${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_CONFIG="$HOME/.config"
BACKUP_DIR="$HOME/.config_backup_$(date +%Y%m%d_%H%M%S)"

# 1. Backup existing configurations
echo -e "\n${YELLOW}==> [1/4] Backing up existing configurations...${NC}"
mkdir -p "$BACKUP_DIR"
for dir in hypr waybar wofi dunst swaync gtk-3.0 gtk-4.0 Thunar xfce4 xdg-desktop-portal; do
    if [ -d "$TARGET_CONFIG/$dir" ]; then
        echo "    Backing up $dir -> $BACKUP_DIR/$dir"
        cp -r "$TARGET_CONFIG/$dir" "$BACKUP_DIR/"
    fi
done
echo -e "${GREEN}    Backup completed in: $BACKUP_DIR${NC}"

# 2. Deploy .config files
echo -e "\n${YELLOW}==> [2/4] Deploying configuration files to $TARGET_CONFIG...${NC}"
mkdir -p "$TARGET_CONFIG"
cp -r "$SCRIPT_DIR/.config/"* "$TARGET_CONFIG/"
echo -e "${GREEN}    Configurations copied successfully.${NC}"

# 3. Set executable permissions
echo -e "\n${YELLOW}==> [3/4] Setting execution permissions on custom scripts...${NC}"
chmod +x "$TARGET_CONFIG/hypr/scripts/"*
echo -e "${GREEN}    Permissions set.${NC}"

# 4. Check syntax and optionally reload
echo -e "\n${YELLOW}==> [4/4] Validating Hyprland configuration syntax...${NC}"
if command -v Hyprland >/dev/null 2>&1; then
    Hyprland --verify-config
    echo -e "${GREEN}    Hyprland syntax is OK!${NC}"
else
    echo "    Hyprland command not in PATH, skipping verify."
fi

# Optional live reload
if command -v hyprctl >/dev/null 2>&1 && [ -n "$HYPRLAND_INSTANCE_SIGNATURE" ]; then
    echo -e "\n${BLUE}==> Hyprland active session detected. Reloading now...${NC}"
    hyprctl reload || true
    killall -SIGUSR2 waybar 2>/dev/null || true
    echo -e "${GREEN}    Hyprland & Waybar reloaded!${NC}"
fi

echo -e "\n${GREEN}==========================================================${NC}"
echo -e "${GREEN}   Deployment Complete! Enjoy your Hyprland Setup!        ${NC}"
echo -e "${GREEN}==========================================================${NC}"
