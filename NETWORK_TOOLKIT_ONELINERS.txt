===============================================================================
       BARNEY FIELD APPLIANCE // ENTERPRISE NETWORK ONE-LINER CHEATSHEET
===============================================================================

1. VENDOR & SWITCH DISCOVERY (Cisco, HP, Aruba, Juniper, WatchGuard, UniFi)
-------------------------------------------------------------------------------
  Query Neighbor Switch & Port:  sudo lldpctl
  Cisco CDP Discovery Packet:    sudo cdpr -d eth0
  SNMP Walk Switch Hostname:     snmpwalk -v2c -c public <SWITCH_IP> sysName
  SNMP Query Port Descriptions:  snmpwalk -v2c -c public <SWITCH_IP> IF-MIB::ifDescr
  SNMP Query Interface Status:   snmpwalk -v2c -c public <SWITCH_IP> IF-MIB::ifOperStatus

2. PACKET CAPTURE & LIVE PAYLOAD GREP (tcpdump, tshark, ngrep)
-------------------------------------------------------------------------------
  Capture DNS Queries Live:      sudo tcpdump -i eth0 -n port 53
  Capture Live HTTP GET/POST:    sudo ngrep -d eth0 -W byline 'GET|POST' port 80
  Capture 802.1X / EAPOL Auth:   sudo tshark -i eth0 -f "ether proto 0x888e"
  Capture DHCP Lease Traffic:    sudo tshark -i eth0 -Y "dhcp"
  Capture SYN Packets to PCAP:   sudo tcpdump -i eth0 -n "tcp[tcpflags] & tcp-syn != 0" -w syn.pcap

3. FIREWALL PROBING, PING & SCANNING (hping3, nmap, mtr, nc)
-------------------------------------------------------------------------------
  TCP SYN Probe Port 443:        sudo hping3 -S -p 443 <TARGET_IP> -c 4
  UDP Port Listener Test:        nc -zuv <TARGET_IP> 53
  Path Latency & Loss Report:    mtr -rw <TARGET_IP>
  Subnet Active Host Discovery:  nmap -sn 192.168.1.0/24
  Quick Port Scan Top 100:       nmap -sS -F <TARGET_IP>
  Service Version Identification:nmap -sV -p 22,80,443,161,2001 <TARGET_IP>

4. MAC SPOOFING & DUAL-NIC INLINE MITM TAP MODE (macchanger, bridge-utils)
-------------------------------------------------------------------------------
  Randomize MAC (Bypass NAC):    sudo macchanger -r eth0
  Set Specific MAC Address:      sudo macchanger -m aa:bb:cc:dd:ee:ff eth0
  Restore Factory Vendor MAC:    sudo macchanger -p eth0
  Start Inline Transparent Tap:  sudo brctl addbr br-tap && sudo brctl addif br-tap eth0 eth1 && sudo ip link set dev br-tap up
  Capture Inline Tap Traffic:    sudo tcpdump -i br-tap -w inline_tap.pcap

5. CONFIG & FIRMWARE FILE TRANSFER (TFTP, FTP, LFTP)
-------------------------------------------------------------------------------
  Download Config via TFTP:      tftp <ROUTER_IP> -c get cisco-config.cfg
  Upload Firmware via TFTP:      tftp <ROUTER_IP> -c put firmware.bin
  Interactive Multi-SFTP/FTP:    lftp -u admin,password sftp://<ROUTER_IP>

6. NETBIOS, SMB & ACTIVE DIRECTORY AUDITING (nbtscan, smbclient)
-------------------------------------------------------------------------------
  Scan NetBIOS Names & MACs:     nbtscan 192.168.1.0/24
  List Shares on SMB Target:     smbclient -L //<TARGET_IP> -U "guest%"

7. SERIAL CONSOLE & OUT-OF-BAND ACCESS (picocom, minicom, telnet)
-------------------------------------------------------------------------------
  Connect Cisco/HP Serial (9600):picocom -b 9600 /dev/ttyCONSOLE
  Connect High-Speed Serial:     picocom -b 115200 /dev/ttyCONSOLE
  Telnet to ser2net Bridge:      telnet <PI_IP> 2001
===============================================================================
