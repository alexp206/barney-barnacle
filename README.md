===============================================================================
               BARNEY FIELD APPLIANCE // QUICK REFERENCE CHEATSHEET
===============================================================================

1. LIVE WEB DIAGNOSTIC DASHBOARD
-------------------------------------------------------------------------------
  Web Interface:           http://<PI_IP>:8888/  or  http://barnacle.netbird.cloud:8888/
  Features:                Live System Health (Uptime, Temp, CPU, RAM, OverlayFS),
                           Interface Telemetry (ETH0, WLAN0, NetBird wt0),
                           Dedicated NetBird Mesh VPN Status Card,
                           LLDP Switch & Port Discovery, Interactive Ping Tool,
                           One-Click Wi-Fi Mode Toggle, Release/Renew DHCP,
                           Enable/Disable Read-Only OS, GitHub Self-Updater.

2. WI-FI MODE TOGGLE (`barney-wifi`)
-------------------------------------------------------------------------------
  Check Wi-Fi Status:      barney-wifi status
  Switch to NAT Hotspot:   sudo barney-wifi hotspot
                           (SSID: Barney-Field-Net / Pass: ??open4ME!!123)
  Switch to LAN Bridge:    sudo barney-wifi hotspot-bridge
                           (Transparent Ethernet-to-Wi-Fi Layer-2 Bridge, No NAT)
  Switch to Client Mode:   sudo barney-wifi client

3. GITHUB SELF-UPDATER (`update.sh`)
-------------------------------------------------------------------------------
  GitHub Repository:       https://github.com/alexp206/barney-barnacle
  One-Click Dashboard:     Click "☁️ Sync & Update GitHub" on Web Dashboard (Port 8888)
  CLI Update Command:      sudo bash /opt/barney/update.sh

4. MINISERVE FIRMWARE HTTP FILE SERVER
-------------------------------------------------------------------------------
  Web Interface:           http://<PI_IP>:8080/
  Firmware Directory:      /srv/firmware
  Features:                Drag-and-drop file upload, search, zip download.
  To add files via CLI:    cp my_firmware.bin /srv/firmware/

5. SERIAL CONSOLE BRIDGE (ser2net)
-------------------------------------------------------------------------------
  Telnet/TCP Port:         2001
  Device Path:             /dev/ttyCONSOLE (auto-linked via udev rule)
  Baud Rate:               9600 8N1
  Usage:                   telnet <PI_IP> 2001

6. BLUETOOTH OUT-OF-BAND CONSOLE
-------------------------------------------------------------------------------
  Service:                 barney-bluetooth-console.service
  Pairing Name:            Barney
  Terminal:                rfcomm0 (115200 baud)
  Usage:                   Pair laptop/phone via Bluetooth -> open Serial Terminal.

7. NETWORK & TELEMETRY TOOLKIT
-------------------------------------------------------------------------------
  LLDP Switch Discovery:   sudo lldpctl
  Packet Capture:          tcpdump -i eth0  /  tshark
  Bandwidth Test:          iperf3 -s (or iperf3 -c <target>)
  Ping & Route:            mtr <target_ip>  /  traceroute <target_ip>
  NetBird Mesh VPN:        netbird status

8. POWER & OVERLAY FS (READ-ONLY PROTECTION)
-------------------------------------------------------------------------------
  Web Toggle:              Click Enable/Disable Read-Only OS on Web Dashboard
  CLI Enable Read-Only:    sudo raspi-config nonint enable_overlayfs
  CLI Disable Read-Only:   sudo raspi-config nonint disable_overlayfs

9. ONBOARD LED STATUS INDICATORS
-------------------------------------------------------------------------------
  Green ACT LED (Heartbeat): Double-blinks when NetBird VPN is Connected.
  Red PWR LED (Solid ON):    Normal power & Internet connectivity OK.
  Red PWR LED (Rapid Flash): Network / Internet Disconnection Failure.
===============================================================================
