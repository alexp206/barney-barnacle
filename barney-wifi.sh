#!/bin/bash
# Barney Wi-Fi Mode Toggle Utility
# Usage: barney-wifi {hotspot|hotspot-bridge|client|status}

ACTION="${1:-status}"

# Detect physical ethernet interface name dynamically (eth0, enxb827eb1b255f, etc.)
ETH_IFACE=$(ip -4 -j addr show | grep -oP '"ifname":"(eth\d+|en[^"]+)"' | head -n1 | cut -d'"' -f4)
ETH_IFACE="${ETH_IFACE:-eth0}"

case "$ACTION" in
    hotspot)
        echo "[INFO] Switching wlan0 to NAT Hotspot mode..."
        pkill parprouted 2>/dev/null
        pkill dhcp-helper 2>/dev/null
        nmcli connection down Hotspot-Bridge 2>/dev/null
        nmcli device disconnect wlan0 2>/dev/null
        if nmcli connection show Hotspot &>/dev/null; then
            nmcli connection up Hotspot
        else
            nmcli device wifi hotspot ifname wlan0 ssid "Barney-Field-Net" password "??open4ME!!123"
        fi
        echo "[SUCCESS] wlan0 is now broadcasting NAT Hotspot (10.42.0.x)!"
        ;;
    hotspot-bridge)
        echo "[INFO] Switching wlan0 to LAN Transparent Bridge mode (no NAT)..."
        nmcli connection down Hotspot 2>/dev/null
        if ! nmcli connection show Hotspot-Bridge &>/dev/null; then
            nmcli connection add type wifi mode ap con-name Hotspot-Bridge ifname wlan0 ssid "Barney-LAN-Bridge" -- wifi-security.key-mgmt wpa-psk wifi-security.psk "??open4ME!!123" ipv4.method link-local
        fi
        nmcli connection up Hotspot-Bridge
        sysctl -w net.ipv4.conf.all.proxy_arp=1 &>/dev/null
        parprouted wlan0 "$ETH_IFACE" &
        dhcp-helper -i wlan0 -b "$ETH_IFACE" &
        echo "[SUCCESS] wlan0 is now broadcasting Barney-LAN-Bridge connected directly to LAN ($ETH_IFACE)!"
        ;;
    client)
        echo "[INFO] Disabling Hotspot and switching wlan0 to Client mode..."
        pkill parprouted 2>/dev/null
        pkill dhcp-helper 2>/dev/null
        nmcli connection down Hotspot 2>/dev/null
        nmcli connection down Hotspot-Bridge 2>/dev/null
        nmcli device connect wlan0 2>/dev/null
        echo "[SUCCESS] wlan0 is now in Client mode!"
        ;;
    status)
        echo "=========================================="
        echo "       BARNEY WI-FI STATUS SUMMARY        "
        echo "=========================================="
        nmcli device status | grep -E "DEVICE|wlan0|eth|en"
        echo ""
        echo "Active Connections:"
        nmcli connection show --active
        ;;
    *)
        echo "Usage: barney-wifi {hotspot|hotspot-bridge|client|status}"
        exit 1
        ;;
esac
