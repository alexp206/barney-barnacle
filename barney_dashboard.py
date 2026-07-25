#!/usr/bin/env python3
import http.server
import socketserver
import json
import subprocess
import os
import re
import time

PORT = 8888

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barney // Field Appliance Telemetry Dashboard</title>
    <style>
        :root {
            --bg-color: #090d16;
            --card-bg: #111827;
            --card-border: #1f2937;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 1.5rem;
            line-height: 1.5;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid var(--card-border);
            margin-bottom: 1.5rem;
        }

        .brand { display: flex; align-items: center; gap: 0.75rem; }

        .brand-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.3rem;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
        }

        h1 { font-size: 1.4rem; font-weight: 700; letter-spacing: 0.5px; }
        .subtitle { font-size: 0.85rem; color: var(--text-muted); }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--accent-green);
            padding: 0.4rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-green);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.25rem;
        }

        @media (max-width: 1400px) {
            .grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.85rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--card-border);
        }

        .card-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .data-list { list-style: none; }
        .data-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.45rem 0;
            font-size: 0.85rem;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.05);
        }
        .data-item:last-child { border-bottom: none; }

        .label { color: var(--text-muted); }
        .value { font-weight: 600; font-family: monospace; }

        .progress-bar-bg {
            width: 80px;
            height: 8px;
            background-color: #1f2937;
            border-radius: 4px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-left: 6px;
        }
        .progress-bar-fill {
            height: 100%;
            background-color: var(--accent-blue);
            transition: width 0.3s ease;
        }

        .tag {
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .tag-blue { background-color: rgba(59, 130, 246, 0.15); color: var(--accent-blue); }
        .tag-purple { background-color: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }
        .tag-green { background-color: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
        .tag-amber { background-color: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
        .tag-red { background-color: rgba(239, 68, 68, 0.15); color: var(--accent-red); }

        .btn-group { display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }

        button {
            flex: 1;
            min-width: 90px;
            padding: 0.55rem 0.75rem;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.78rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-primary { background-color: var(--accent-blue); color: white; }
        .btn-primary:hover { background-color: #2563eb; }

        .btn-purple { background-color: var(--accent-purple); color: white; }
        .btn-purple:hover { background-color: #7c3aed; }

        .btn-secondary { background-color: #374151; color: white; }
        .btn-secondary:hover { background-color: #4b5563; }

        .input-group {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }
        input[type="text"] {
            flex: 1;
            background-color: #05070e;
            border: 1px solid var(--card-border);
            border-radius: 6px;
            padding: 0.45rem 0.75rem;
            color: var(--text-main);
            font-family: monospace;
            font-size: 0.85rem;
        }

        pre {
            background-color: #05070e;
            padding: 0.75rem;
            border-radius: 6px;
            font-size: 0.8rem;
            color: #10b981;
            overflow-x: auto;
            max-height: 220px;
        }

        footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <div class="brand-icon">⚡</div>
            <div>
                <h1>BARNEY FIELD DIAGNOSTIC APPLIANCE v1.1 🚀</h1>
                <div class="subtitle">Live System Hardware, Network & Services Dashboard</div>
            </div>
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center;">
            <div id="update-badge"></div>
            <button class="btn-primary" style="background-color: #059669; padding: 0.4rem 0.85rem;" onclick="syncFromGithub()">☁️ Sync & Update GitHub</button>
            <div class="status-badge">
                <div class="dot"></div>
                <span id="system-status">SYSTEM ONLINE</span>
            </div>
        </div>
    </header>

    <div class="grid">
        <!-- 1. System Hardware & Health -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">🖥️ System Health & Storage</div>
            </div>
            <ul class="data-list">
                <li class="data-item"><span class="label">Uptime</span><span class="value" id="sys-uptime">Loading...</span></li>
                <li class="data-item"><span class="label">SoC Temp</span><span class="value" id="sys-temp">...</span></li>
                <li class="data-item"><span class="label">CPU Load</span><span class="value" id="sys-load">...</span></li>
                <li class="data-item">
                    <span class="label">RAM Usage</span>
                    <span class="value"><span id="sys-ram-text">...</span><div class="progress-bar-bg"><div class="progress-bar-fill" id="ram-bar" style="width:0%;"></div></div></span>
                </li>
                <li class="data-item"><span class="label">OverlayFS Protection</span><span class="value" id="sys-overlay">...</span></li>
            </ul>
            <div class="btn-group">
                <button class="btn-purple" onclick="setOverlayMode('enable')">Enable Read-Only OS</button>
                <button class="btn-secondary" onclick="setOverlayMode('disable')">Disable Read-Only OS</button>
            </div>
        </div>

        <!-- 2. Network Interfaces & Connectivity -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">🌐 Network Telemetry</div>
            </div>
            <ul class="data-list">
                <li class="data-item"><span class="label">Ethernet IP</span><span class="value" id="ip-eth0">Loading...</span></li>
                <li class="data-item"><span class="label">WLAN0 (Wi-Fi IP)</span><span class="value" id="ip-wlan0">Loading...</span></li>
                <li class="data-item"><span class="label">WT0 (NetBird IP)</span><span class="value" id="ip-netbird">Loading...</span></li>
                <li class="data-item"><span class="label">Internet Latency</span><span class="value" id="net-latency">...</span></li>
                <li class="data-item"><span class="label">Gateway</span><span class="value" id="net-gateway">...</span></li>
            </ul>
            <div class="btn-group">
                <button class="btn-secondary" onclick="renewDhcp()">🔄 Release / Renew DHCP</button>
            </div>
        </div>

        <!-- 3. Dedicated NetBird Card -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">🦅 NetBird Mesh VPN</div>
            </div>
            <ul class="data-list">
                <li class="data-item"><span class="label">NetBird IP</span><span class="value" id="nb-ip">Loading...</span></li>
                <li class="data-item"><span class="label">FQDN Host</span><span class="value" id="nb-fqdn">...</span></li>
                <li class="data-item"><span class="label">Management</span><span class="value" id="nb-mgmt">...</span></li>
                <li class="data-item"><span class="label">Connected Peers</span><span class="value" id="nb-peers">...</span></li>
            </ul>
        </div>

        <!-- 4. LLDP Switch & Port Discovery -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">🔌 LLDP Switch Telemetry</div>
            </div>
            <ul class="data-list">
                <li class="data-item"><span class="label">Switch Name</span><span class="value" id="lldp-switch">Searching...</span></li>
                <li class="data-item"><span class="label">Port ID</span><span class="value" id="lldp-port">N/A</span></li>
                <li class="data-item"><span class="label">VLAN Tag</span><span class="value" id="lldp-vlan">Untagged</span></li>
            </ul>
        </div>

        <!-- 5. Wi-Fi Mode & Access Point Controls -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">📡 Wi-Fi Mode & Controls</div>
            </div>
            <ul class="data-list">
                <li class="data-item"><span class="label">Current Mode</span><span class="value"><span class="tag tag-blue" id="wifi-mode">Checking...</span></span></li>
                <li class="data-item"><span class="label">Active SSID</span><span class="value" id="wifi-ssid">...</span></li>
            </ul>
            <div class="btn-group">
                <button class="btn-primary" onclick="setWifiMode('hotspot')">NAT Hotspot (10.42.0.x)</button>
                <button class="btn-purple" onclick="setWifiMode('hotspot-bridge')">LAN Bridge (No NAT)</button>
                <button class="btn-secondary" onclick="setWifiMode('client')">Client Mode</button>
            </div>
        </div>

        <!-- 6. Active Field Services Status -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">⚙️ Active Field Services</div>
            </div>
            <ul class="data-list">
                <li class="data-item"><span class="label">NetBird Mesh VPN</span><span class="value" id="svc-netbird"><span class="tag tag-green">Connected</span></span></li>
                <li class="data-item"><span class="label">Miniserve Web Server</span><span class="value"><span class="tag tag-green">Port 8080 (/srv/firmware)</span></span></li>
                <li class="data-item"><span class="label">Serial Console Bridge</span><span class="value" id="svc-serial">Checking...</span></li>
                <li class="data-item"><span class="label">Bluetooth Console</span><span class="value"><span class="tag tag-blue">RFCOMM 115200</span></span></li>
            </ul>
        </div>

        <!-- 7. Interactive Field Diagnostics Tool -->
        <div class="card" style="grid-column: span 2;">
            <div class="card-header">
                <div class="card-title">🔍 Quick Ping & Network Diagnostics</div>
            </div>
            <div class="input-group">
                <input type="text" id="ping-target" placeholder="Target IP / Hostname (e.g. 192.168.1.1)" value="1.1.1.1">
                <button class="btn-primary" style="flex: none; padding: 0.45rem 1rem;" onclick="runPingTest()">Run Ping</button>
            </div>
            <pre id="ping-output" style="margin-top: 0.75rem; max-height: 90px;">Click "Run Ping" to test connectivity to target IP.</pre>
        </div>
    </div>

    <div class="card" style="margin-top: 1.25rem;">
        <div class="card-header">
            <div class="card-title">📊 Raw Diagnostic Console Output</div>
            <button class="btn-secondary" style="flex: none; padding: 0.3rem 0.8rem;" onclick="fetchStatus()">Refresh Telemetry</button>
        </div>
        <pre id="raw-log">Fetching diagnostic telemetry...</pre>
    </div>

    <footer>
        Barney Field Appliance • Auto-refreshes telemetry every 5 seconds
    </footer>

    <script>
        async function fetchStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                
                document.getElementById('sys-uptime').innerText = data.uptime || 'N/A';
                document.getElementById('sys-temp').innerText = data.soc_temp ? data.soc_temp + ' °C' : 'N/A';
                document.getElementById('sys-load').innerText = data.load_avg || '...';
                
                document.getElementById('sys-ram-text').innerText = (data.ram_pct || 0) + '%';
                document.getElementById('ram-bar').style.width = (data.ram_pct || 0) + '%';

                document.getElementById('sys-overlay').innerHTML = data.overlay_active
                    ? '<span class="tag tag-purple">Protected (Read-Only)</span>'
                    : '<span class="tag tag-green">Persistent (Read-Write)</span>';

                if (data.update_status === 'update_available') {
                    document.getElementById('update-badge').innerHTML = '<span class="tag tag-purple">Update Available!</span>';
                } else if (data.update_status === 'up_to_date') {
                    document.getElementById('update-badge').innerHTML = '<span class="tag tag-green">Up to Date (' + (data.update_commit || '') + ')</span>';
                } else {
                    document.getElementById('update-badge').innerText = '';
                }

                document.getElementById('ip-eth0').innerText = data.ip_eth0 || 'Disconnected';
                document.getElementById('ip-wlan0').innerText = data.ip_wlan0 || 'Disconnected';
                document.getElementById('ip-netbird').innerText = data.ip_netbird || 'Disconnected';

                document.getElementById('nb-ip').innerText = data.nb_ip || 'Disconnected';
                document.getElementById('nb-fqdn').innerText = data.nb_fqdn || 'N/A';
                document.getElementById('nb-mgmt').innerHTML = data.nb_mgmt === 'Connected' 
                    ? '<span class="tag tag-green">Connected</span>' 
                    : '<span class="tag tag-red">Disconnected</span>';
                document.getElementById('nb-peers').innerText = data.nb_peers || '0/0';

                document.getElementById('net-latency').innerText = data.ping_latency || 'Offline';
                document.getElementById('net-gateway').innerText = data.default_gw || 'None';

                document.getElementById('wifi-mode').innerText = data.wifi_mode || 'Unknown';
                document.getElementById('wifi-ssid').innerText = data.wifi_ssid || 'None';

                document.getElementById('lldp-switch').innerText = data.lldp_switch || 'No Switch Info';
                document.getElementById('lldp-port').innerText = data.lldp_port || 'N/A';
                document.getElementById('lldp-vlan').innerText = data.lldp_vlan || 'Untagged';

                document.getElementById('svc-serial').innerHTML = data.serial_connected 
                    ? '<span class="tag tag-green">/dev/ttyCONSOLE Connected</span>' 
                    : '<span class="tag tag-amber">No USB Serial Adapter</span>';

                document.getElementById('raw-log').innerText = data.raw_summary || 'No log data';
            } catch (err) {
                console.error(err);
            }
        }

        async function syncFromGithub() {
            if (!confirm('Pull latest updates from GitHub and restart services?')) return;
            try {
                const res = await fetch('/api/git_update', { method: 'POST' });
                const result = await res.json();
                alert(result.message);
                setTimeout(fetchStatus, 3000);
            } catch (err) {
                alert('Error syncing from GitHub: ' + err);
            }
        }

        async function setOverlayMode(action) {
            let msg = action === 'enable' ? 'Enable Read-Only OverlayFS Mode? (Requires reboot)' : 'Disable Read-Only Mode and make SD card Read-Write? (Requires reboot)';
            if (!confirm(msg)) return;
            try {
                const res = await fetch('/api/overlayfs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: action })
                });
                const result = await res.json();
                alert(result.message);
                fetchStatus();
            } catch (err) {
                alert('Error toggling OverlayFS: ' + err);
            }
        }

        async function setWifiMode(mode) {
            let label = mode === 'hotspot-bridge' ? 'LAN Bridge Mode (No NAT)' : (mode === 'hotspot' ? 'NAT Hotspot Mode' : 'Client Mode');
            if (!confirm(`Switch Wi-Fi to ${label}?`)) return;
            try {
                const res = await fetch('/api/wifi_mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: mode })
                });
                const result = await res.json();
                alert(result.message);
                fetchStatus();
            } catch (err) {
                alert('Error changing Wi-Fi mode: ' + err);
            }
        }

        async function renewDhcp() {
            if (!confirm('Re-request DHCP lease on Ethernet interface?')) return;
            try {
                const res = await fetch('/api/dhcp_renew', { method: 'POST' });
                const result = await res.json();
                alert(result.message);
                setTimeout(fetchStatus, 3000);
            } catch (err) {
                alert('Error renewing DHCP: ' + err);
            }
        }

        async function runPingTest() {
            const target = document.getElementById('ping-target').value.trim();
            if (!target) return;
            const outputEl = document.getElementById('ping-output');
            outputEl.innerText = `Pinging ${target}...`;
            try {
                const res = await fetch('/api/ping?target=' + encodeURIComponent(target));
                const data = await res.json();
                outputEl.innerText = data.output;
            } catch (err) {
                outputEl.innerText = 'Error running ping: ' + err;
            }
        }

        fetchStatus();
        setInterval(fetchStatus, 5000);
    </script>
</body>
</html>
"""

def get_sys_metrics():
    uptime = "N/A"
    try:
        with open("/proc/uptime", "r") as f:
            seconds = float(f.readline().split()[0])
            uptime = f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"
    except Exception: pass

    temp_c = None
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_c = round(float(f.read().strip()) / 1000.0, 1)
    except Exception: pass

    load_avg = "N/A"
    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.readline().split()
            load_avg = f"{parts[0]} / {parts[1]} / {parts[2]}"
    except Exception: pass

    ram_pct = 0
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
            mem_total = int([l for l in lines if "MemTotal:" in l][0].split()[1])
            mem_avail = int([l for l in lines if "MemAvailable:" in l][0].split()[1])
            ram_pct = round(((mem_total - mem_avail) / mem_total) * 100, 1)
    except Exception: pass

    overlay_active = False
    try:
        with open("/proc/mounts", "r") as f:
            overlay_active = "overlayroot" in f.read() or "overlay" in f.read()
    except Exception: pass

    return uptime, temp_c, load_avg, ram_pct, overlay_active

def get_update_status():
    status = "up_to_date"
    commit = ""
    try:
        if os.path.exists("/tmp/barney_update_status.json"):
            with open("/tmp/barney_update_status.json", "r") as f:
                data = json.load(f)
                status = data.get("status", "up_to_date")
                commit = data.get("local_commit", "")
    except Exception: pass
    return status, commit

def get_ip(interface_type):
    try:
        out = subprocess.check_output(["ip", "-4", "-j", "addr", "show"], stderr=subprocess.DEVNULL).decode()
        data = json.loads(out)
        for iface in data:
            ifname = iface.get("ifname", "")
            if interface_type == "eth" and (ifname.startswith("eth") or ifname.startswith("en")) and ifname != "lo":
                addr_info = iface.get("addr_info", [])
                if addr_info:
                    return f"{addr_info[0].get('local', 'Disconnected')} ({ifname})"
            elif interface_type == "wlan" and ifname.startswith("wlan"):
                addr_info = iface.get("addr_info", [])
                if addr_info:
                    return f"{addr_info[0].get('local', 'Disconnected')} ({ifname})"
            elif interface_type == "netbird" and (ifname.startswith("wt") or ifname.startswith("netbird")):
                addr_info = iface.get("addr_info", [])
                if addr_info:
                    return addr_info[0].get('local', 'Disconnected')
    except Exception:
        pass
    return "Disconnected"

def get_netbird_details():
    ip = "Disconnected"
    fqdn = "N/A"
    mgmt = "Disconnected"
    peers = "0/0"
    raw = "NetBird offline"
    try:
        raw = subprocess.check_output(["netbird", "status"], stderr=subprocess.DEVNULL).decode()
        for line in raw.splitlines():
            if "NetBird IP:" in line:
                ip = line.split("NetBird IP:")[1].strip()
            elif "FQDN:" in line:
                fqdn = line.split("FQDN:")[1].strip()
            elif "Management:" in line:
                mgmt = line.split("Management:")[1].strip()
            elif "Peers count:" in line:
                peers = line.split("Peers count:")[1].strip()
    except Exception: pass
    return ip, fqdn, mgmt, peers, raw

def get_eth_ifname():
    try:
        out = subprocess.check_output(["ip", "-4", "-j", "addr", "show"], stderr=subprocess.DEVNULL).decode()
        data = json.loads(out)
        for iface in data:
            ifname = iface.get("ifname", "")
            if (ifname.startswith("eth") or ifname.startswith("en")) and ifname != "lo":
                return ifname
    except Exception: pass
    return "eth0"

def get_default_gw_and_ping():
    gw = "None"
    latency = "Offline"
    try:
        out = subprocess.check_output(["ip", "route", "show", "default"], stderr=subprocess.DEVNULL).decode()
        if "via" in out:
            gw = out.split("via")[1].split()[0]
    except Exception: pass

    try:
        out = subprocess.check_output(["ping", "-c", "1", "-W", "2", "1.1.1.1"], stderr=subprocess.DEVNULL).decode()
        match = re.search(r"time=([\d\.]+)\s*ms", out)
        if match:
            latency = f"{match.group(1)} ms"
    except Exception: pass

    return gw, latency

def get_lldp():
    try:
        out = subprocess.check_output(["lldpctl", "-f", "json"], stderr=subprocess.DEVNULL).decode()
        data = json.loads(out)
        
        ifaces = data.get("lldp", {}).get("interface", {})
        if not ifaces:
            return "No Switch Info", "N/A", "Untagged"
            
        if isinstance(ifaces, dict):
            iface_val = list(ifaces.values())[0]
        elif isinstance(ifaces, list):
            iface_val = ifaces[0]
        else:
            return "No Switch Info", "N/A", "Untagged"

        chassis_dict = iface_val.get("chassis", {})
        sys_name = "No Switch Info"
        if isinstance(chassis_dict, dict) and chassis_dict:
            first_chassis_key = list(chassis_dict.keys())[0]
            first_chassis = chassis_dict[first_chassis_key]
            if isinstance(first_chassis, dict) and "name" in first_chassis:
                sys_name = first_chassis.get("name", {}).get("value", first_chassis_key)
            else:
                sys_name = first_chassis_key

        port_dict = iface_val.get("port", {})
        port_id = "N/A"
        if isinstance(port_dict, dict):
            port_id = port_dict.get("id", {}).get("value", "N/A")

        vlan_dict = iface_val.get("vlan", {})
        vlan_id = "Untagged"
        if isinstance(vlan_dict, dict):
            vlan_id = str(vlan_dict.get("vlan-id", "Untagged"))

        return sys_name, port_id, vlan_id
    except Exception as e:
        return "Searching...", "N/A", "Untagged"

def get_wifi_info():
    try:
        out = subprocess.check_output(["barney-wifi", "status"], stderr=subprocess.DEVNULL).decode()
        if "Hotspot-Bridge" in out:
            mode = "LAN Bridge (No NAT)"
            ssid = "Barney-LAN-Bridge"
        elif "Hotspot" in out:
            mode = "NAT Hotspot"
            ssid = "Barney-Field-Net"
        else:
            mode = "Client Mode"
            ssid_match = re.search(r"wlan0\s+wifi\s+connected\s+(.+)", out)
            ssid = ssid_match.group(1).strip() if ssid_match else "Scanning"
        return mode, ssid, out
    except Exception:
        return "Client Mode", "N/A", "barney-wifi status unavailable"

class BarneyDashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path == '/api/status':
            uptime, temp_c, load_avg, ram_pct, overlay_active = get_sys_metrics()
            up_status, up_commit = get_update_status()
            eth0_ip = get_ip("eth")
            wlan0_ip = get_ip("wlan")
            netbird_ip = get_ip("netbird")
            nb_ip, nb_fqdn, nb_mgmt, nb_peers, netbird_raw = get_netbird_details()
            gw, latency = get_default_gw_and_ping()
            switch_name, port_id, vlan = get_lldp()
            wifi_mode, wifi_ssid, wifi_raw = get_wifi_info()
            serial_conn = os.path.exists('/dev/ttyCONSOLE')

            summary = f"=== WI-FI STATUS ===\n{wifi_raw}\n\n=== NETBIRD VPN STATUS ===\n{netbird_raw}"

            data = {
                "uptime": uptime,
                "soc_temp": temp_c,
                "load_avg": load_avg,
                "ram_pct": ram_pct,
                "overlay_active": overlay_active,
                "update_status": up_status,
                "update_commit": up_commit,
                "ip_eth0": eth0_ip,
                "ip_wlan0": wlan0_ip,
                "ip_netbird": netbird_ip,
                "nb_ip": nb_ip,
                "nb_fqdn": nb_fqdn,
                "nb_mgmt": nb_mgmt,
                "nb_peers": nb_peers,
                "default_gw": gw,
                "ping_latency": latency,
                "wifi_mode": wifi_mode,
                "wifi_ssid": wifi_ssid,
                "lldp_switch": switch_name,
                "lldp_port": port_id,
                "lldp_vlan": vlan,
                "serial_connected": serial_conn,
                "raw_summary": summary
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path.startswith('/api/ping'):
            target = "1.1.1.1"
            if "?" in self.path:
                q = self.path.split("?")[1]
                for param in q.split("&"):
                    if param.startswith("target="):
                        target = param.split("=")[1]
            try:
                target_clean = re.sub(r"[^a-zA-Z0-9\.\-]", "", target)
                out = subprocess.check_output(["ping", "-c", "4", target_clean], stderr=subprocess.STDOUT, timeout=5).decode()
            except Exception as e:
                out = f"Ping failed or timed out: {e}"

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"output": out}).encode('utf-8'))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/wifi_mode':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            try:
                req = json.loads(body)
                mode = req.get("mode", "client")
                out = subprocess.check_output(["sudo", "barney-wifi", mode], stderr=subprocess.STDOUT).decode()
                res = {"status": "ok", "message": out}
            except Exception as e:
                res = {"status": "error", "message": str(e)}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
        elif self.path == '/api/overlayfs':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            try:
                req = json.loads(body)
                action = req.get("action", "disable")
                cmd = "enable_overlayfs" if action == "enable" else "disable_overlayfs"
                out = subprocess.check_output(["sudo", "raspi-config", "nonint", cmd], stderr=subprocess.STDOUT).decode()
                state_str = "ENABLED (Read-Only OS)" if action == "enable" else "DISABLED (Read-Write OS)"
                res = {"status": "ok", "message": f"Read-Only OverlayFS mode is now {state_str}.\n\nNOTE: Please reboot the Raspberry Pi for this change to take effect."}
            except Exception as e:
                res = {"status": "error", "message": f"Error toggling OverlayFS: {e}"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
        elif self.path == '/api/git_update':
            try:
                subprocess.Popen(["sudo", "bash", "/opt/barney/update.sh"])
                res = {"status": "ok", "message": "GitHub update initiated! Barney will restart in 1 second."}
            except Exception as e:
                res = {"status": "error", "message": f"Error updating from GitHub: {e}"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
        elif self.path == '/api/dhcp_renew':
            try:
                eth_name = get_eth_ifname()
                out = subprocess.check_output(["sudo", "nmcli", "device", "reapply", eth_name], stderr=subprocess.STDOUT).decode()
                res = {"status": "ok", "message": f"DHCP lease renewed on {eth_name}:\n{out}"}
            except Exception as e:
                res = {"status": "error", "message": f"DHCP renew note: {e}"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))

    def log_message(self, format, *args):
        pass

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ReusableTCPServer(("0.0.0.0", PORT), BarneyDashboardHandler) as httpd:
        print(f"Barney Dashboard running on port {PORT}")
        httpd.serve_forever()
