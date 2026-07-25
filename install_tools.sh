#!/bin/bash
# Barney Field Appliance Toolset Installer
# Installs and updates all required enterprise network diagnostic tools

if [ "$EUID" -ne 0 ]; then
    echo "[ERROR] Please run as root (sudo bash install_tools.sh)"
    exit 1
fi

echo "[INFO] Updating package lists..."
apt-get update -qq

PACKAGES=(
    nmap netcat-openbsd lldpd mtr-tiny tcpdump tshark iperf3 traceroute ethtool iproute2
    minicom picocom screen ser2net usbutils network-manager dnsutils whois
    tftp-hpa ftp lftp snmp cdpr ngrep hping3 macchanger bridge-utils nbtscan smbclient socat
    python3-pip python3-pil python3-spidev python3-rpi-lgpio python3-packaging python3-setuptools
    git parprouted dhcp-helper bluetooth bluez bluez-tools
)

echo "[INFO] Ensuring all enterprise diagnostic tools are installed..."
apt-get install -y --no-install-recommends "${PACKAGES[@]}"

echo "[INFO] Enabling and starting lldpd service..."
systemctl enable --now lldpd 2>/dev/null

echo "[SUCCESS] All Barney enterprise diagnostic tools are up-to-date and ready!"
