#!/usr/bin/env bash
# ==============================================================================
# Buzzard Power Suite - Universal Linux Cross-Distro Installer Script
# Supports: Ubuntu, Debian, Pop!_OS, Arch, Manjaro, Fedora, RHEL, openSUSE, etc.
# ==============================================================================

set -e

BOLD="\033[1m"
GREEN="\033[32m"
BLUE="\033[34m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}"
echo "========================================================"
echo "🦅 BUZZARD POWER SUITE - UNIVERSAL LINUX INSTALLER v1.0.0"
echo "========================================================"
echo -e "${RESET}"

# 1. Detect Package Manager and Distro
echo -e "${BLUE}▶ Introspecting Linux Distribution...${RESET}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO_NAME=$NAME
    DISTRO_ID=$ID
else
    DISTRO_NAME="Generic Linux"
    DISTRO_ID="generic"
fi

echo -e "Detected OS: ${GREEN}${DISTRO_NAME}${RESET}"

# 2. Package Installation based on Package Manager
if command -v apt-get &> /dev/null; then
    echo -e "${BLUE}▶ Using APT Package Manager (Debian/Ubuntu/Mint/Pop!_OS)...${RESET}"
    sudo apt-get update -qq
    sudo apt-get install -y -qq tlp powertop x11-xserver-utils libnotify-bin python3-gi gir1.2-appindicator3-0.1 linux-tools-common acpi python3-pip python3-yaml || true

elif command -v pacman &> /dev/null; then
    echo -e "${BLUE}▶ Using PACMAN Package Manager (Arch/Manjaro/EndeavourOS)...${RESET}"
    sudo pacman -Sy --needed --noconfirm tlp powertop xorg-xrandr libnotify python-gobject libappindicator-gtk3 acpi python-pip python-yaml || true

elif command -v dnf &> /dev/null; then
    echo -e "${BLUE}▶ Using DNF Package Manager (Fedora/RHEL/Alma)...${RESET}"
    sudo dnf install -y tlp powertop xrandr libnotify python3-gobject libappindicator-gtk3 kernel-tools acpi python3-pip python3-pyyaml || true

elif command -v zypper &> /dev/null; then
    echo -e "${BLUE}▶ Using ZYPPER Package Manager (openSUSE)...${RESET}"
    sudo zypper install -y tlp powertop xrandr libnotify-tools python3-gobject acpi python3-pip python3-PyYAML || true

else
    echo -e "${YELLOW}Notice: Unknown package manager. Please ensure python3, tlp, and powertop are installed manually.${RESET}"
fi

# 3. Install Buzzard Power Suite Python Package
echo -e "\n${BLUE}▶ Installing Buzzard Power Suite Python Package...${RESET}"
python3 -m pip install --break-system-packages -e . 2>/dev/null || python3 -m pip install -e .

# Ensure $HOME/.local/bin binaries are symlinked to /usr/local/bin so Zsh/Bash/Arch find them instantly
USER_BIN_DIR="$HOME/.local/bin"
if [ -d "$USER_BIN_DIR" ]; then
    if [ -f "$USER_BIN_DIR/buzzard" ]; then
        sudo ln -sf "$USER_BIN_DIR/buzzard" /usr/local/bin/buzzard 2>/dev/null || true
    fi
    if [ -f "$USER_BIN_DIR/buzzard-gui" ]; then
        sudo ln -sf "$USER_BIN_DIR/buzzard-gui" /usr/local/bin/buzzard-gui 2>/dev/null || true
    fi
fi

# Also add ~/.local/bin to shell configuration files if missing
for RC_FILE in "$HOME/.zshrc" "$HOME/.bashrc"; do
    if [ -f "$RC_FILE" ] && ! grep -q '\.local/bin' "$RC_FILE"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
    fi
done

# 4. Configure Passwordless Power Sysfs Privileges
echo -e "\n${BLUE}▶ Setting up Passwordless Sudoers Power Privileges...${RESET}"
SUDOERS_FILE="/etc/sudoers.d/buzzard"
SUDOERS_CONTENT="ALL ALL=(ALL) NOPASSWD: /usr/bin/tee, /usr/bin/tlp, /usr/bin/powertop, /usr/bin/powerprofilesctl"

echo "$SUDOERS_CONTENT" | sudo tee $SUDOERS_FILE > /dev/null
sudo chmod 0440 $SUDOERS_FILE

# 5. Enable Systemd Background User Service
echo -e "\n${BLUE}▶ Enabling Systemd User Daemon Service...${RESET}"
"$USER_BIN_DIR/buzzard" setup 2>/dev/null || buzzard setup || true

# 6. Install Desktop Entry for GUI Launcher
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"
cat << EOF > "$DESKTOP_DIR/buzzard.desktop"
[Desktop Entry]
Name=Buzzard Power Suite
Comment=Modular Linux Power Management & Hardware Control Suite
Exec=buzzard-gui
Icon=battery-good-symbolic
Terminal=false
Type=Application
Categories=System;Settings;HardwareSettings;
EOF

echo -e "\n${GREEN}${BOLD}========================================================"
echo "✔ INSTALLATION COMPLETE!"
echo "Run 'buzzard status' or 'buzzard help' to start using Buzzard Power Suite."
echo "Run 'buzzard-gui' to launch the desktop system tray app."
echo "========================================================${RESET}"
