===============================================================================
               BARNEY FIELD APPLIANCE // QUICK REFERENCE CHEATSHEET
===============================================================================

1. WI-FI MODE TOGGLE (`barney-wifi`)
-------------------------------------------------------------------------------
  Check Wi-Fi Status:      barney-wifi status
  Switch to Hotspot Mode:  sudo barney-wifi hotspot
                           (SSID: Barney-Field-Net / Pass: ??open4ME!!123)
  Switch to Client Mode:   sudo barney-wifi client

2. MINISERVE FIRMWARE HTTP FILE SERVER
-------------------------------------------------------------------------------
  Web Interface:           http://<PI_IP>:8080/
  Firmware Directory:      /srv/firmware
  Features:                Drag-and-drop file upload, search, zip download.
  To add files via CLI:    cp my_firmware.bin /srv/firmware/

3. SERIAL CONSOLE BRIDGE (ser2net)
-------------------------------------------------------------------------------
  Telnet/TCP Port:         2001
  Device Path:             /dev/ttyCONSOLE (auto-linked via udev rule)
  Baud Rate:               9600 8N1
  Usage:                   telnet <PI_IP> 2001

4. BLUETOOTH OUT-OF-BAND CONSOLE
-------------------------------------------------------------------------------
  Service:                 barney-bluetooth-console.service
  Pairing Name:            Barney
  Terminal:                rfcomm0 (115200 baud)
  Usage:                   Pair laptop/phone via Bluetooth -> open Serial Terminal.

5. NETWORK & TELEMETRY TOOLKIT
-------------------------------------------------------------------------------
  LLDP Switch Discovery:   sudo lldpctl
  Packet Capture:          tcpdump -i eth0  /  tshark
  Bandwidth Test:          iperf3 -s (or iperf3 -c <target>)
  Ping & Route:            mtr <target_ip>  /  traceroute <target_ip>
  NetBird Mesh VPN:        netbird status

6. e-PAPER DISPLAY & SYSTEMD SERVICES
-------------------------------------------------------------------------------
  Update Display Now:      sudo /usr/bin/python3 /opt/barney/display_status.py
  Display Timer:           barney-display.timer (updates every 3 mins)
  Service Logs:            journalctl -u barney-display -f
                           journalctl -u barney-miniserve -f
                           journalctl -u barney-bluetooth-console -f

7. POWER & OVERLAY FS
-------------------------------------------------------------------------------
  Enable Read-Only FS:     sudo raspi-config nonint enable_overlayfs
  Disable Read-Only FS:    sudo raspi-config nonint disable_overlayfs

8. ONBOARD LED STATUS INDICATORS
-------------------------------------------------------------------------------
  Green ACT LED (Heartbeat): Double-blinks when NetBird VPN is Connected.
  Red PWR LED (Solid ON):    Normal power & Internet connectivity OK.
  Red PWR LED (Rapid Flash): Network / Internet Disconnection Failure.

9. LIVE WEB DIAGNOSTIC DASHBOARD
-------------------------------------------------------------------------------
  URL:                     http://<PI_IP>:8888/
  Features:                Live System Health (Uptime, Temp, CPU Load, RAM, Disk),
                           Interface IPs (ETH0, WLAN0, NetBird wt0), LLDP Switch,
                           Interactive Ping Diagnostics & One-Click Wi-Fi Mode Toggle.
===============================================================================
