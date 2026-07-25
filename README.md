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

3. ENTERPRISE NETWORK DIAGNOSTIC TOOLKIT
-------------------------------------------------------------------------------
  DNS & Domain Lookup:     dig <domain>  /  nslookup <target>  /  whois <domain>
  File Transfer & TFTP:    tftp <host>  /  ftp <host>  /  lftp <host>
  Cisco / HP / Juniper:    sudo lldpctl  (Supports LLDP, CDP, EDP, FDP, SONMP)
                           sudo cdpr -d eth0  (Cisco Discovery Protocol Reporter)
                           snmpwalk -v2c -c public <target_ip>  (SNMP Query)
  Security & Probing:      hping3 -S -p 80 <target>  (Custom TCP/IP probe)
                           macchanger -r eth0  (Spoof MAC address for 802.1X/NAC)
                           ngrep -d eth0 'GET|POST' port 80  (Packet Grep)
                           nbtscan 192.168.1.0/24  /  smbclient -L <ip>
  Packet Capture & Sniff:  tcpdump -i eth0 -w cap.pcap  /  tshark -i eth0
  Bandwidth & Performance: iperf3 -s (or iperf3 -c <target>)
  Ping & Route:            mtr <target_ip>  /  traceroute <target_ip>

4. USB NIC INLINE MAN-IN-THE-MIDDLE (MITM) TAP MODE
-------------------------------------------------------------------------------
  Description:             Plug USB Ethernet adapter (eth1) to bridge inline between
                           a switch and a firewall/router for silent packet tapping.
  Enable Transparent Tap:  sudo brctl addbr br-tap
                           sudo brctl addif br-tap eth0
                           sudo brctl addif br-tap eth1
                           sudo ip link set dev br-tap up
  Capture Inline Traffic:  sudo tcpdump -i br-tap -w tap_traffic.pcap

5. GITHUB SELF-UPDATER (`update.sh`)
-------------------------------------------------------------------------------
  GitHub Repository:       https://github.com/alexp206/barney-barnacle
  One-Click Dashboard:     Click "☁️ Sync & Update GitHub" on Web Dashboard (Port 8888)
  CLI Update Command:      sudo bash /opt/barney/update.sh

6. MINISERVE FIRMWARE HTTP FILE SERVER
-------------------------------------------------------------------------------
  Web Interface:           http://<PI_IP>:8080/
  Firmware Directory:      /srv/firmware
  To add files via CLI:    cp my_firmware.bin /srv/firmware/

7. SERIAL CONSOLE BRIDGE (ser2net)
-------------------------------------------------------------------------------
  Telnet/TCP Port:         2001
  Device Path:             /dev/ttyCONSOLE (auto-linked via udev rule)
  Usage:                   telnet <PI_IP> 2001 (9600 8N1)

8. BLUETOOTH OUT-OF-BAND CONSOLE
-------------------------------------------------------------------------------
  Service:                 barney-bluetooth-console.service
  Pairing Name:            Barney
  Terminal:                rfcomm0 (115200 baud)

9. POWER & OVERLAY FS (READ-ONLY PROTECTION)
-------------------------------------------------------------------------------
  Web Toggle:              Click Enable/Disable Read-Only OS on Web Dashboard
  CLI Enable Read-Only:    sudo raspi-config nonint enable_overlayfs
  CLI Disable Read-Only:   sudo raspi-config nonint disable_overlayfs
===============================================================================
