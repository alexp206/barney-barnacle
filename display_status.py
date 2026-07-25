#!/usr/bin/env python3
import time
import json
import subprocess
import socket
from PIL import Image, ImageDraw, ImageFont

# Waveshare 2.13" 3-color (Red/Black/White) driver
from waveshare_epd import epd2in13b_V4 

def get_ip_address(interface):
    """Fetch IP address for a specific network interface."""
    try:
        out = subprocess.check_output(["ip", "-4", "addr", "show", interface], stderr=subprocess.DEVNULL).decode("utf-8")
        for line in out.splitlines():
            if "inet " in line:
                return line.split()[1].split("/")[0]
    except Exception:
        return "Disconnected"
    return "No IP"

def get_lldp_info():
    """Parse lldpctl JSON output to retrieve Switch Name, Port ID, and VLAN."""
    try:
        out = subprocess.check_output(["lldpctl", "-f", "json"], stderr=subprocess.DEVNULL).decode("utf-8")
        data = json.loads(out)
        interface_data = data.get("lldp", {}).get("interface", {})
        
        if isinstance(interface_data, list):
            interface_data = interface_data[0]
            
        eth_info = interface_data.get("eth0", {})
        sys_name = eth_info.get("chassis", {}).get("name", {}).get("value", "No Switch Info")
        port_id = eth_info.get("port", {}).get("id", {}).get("value", "N/A")
        
        # Extract VLAN if present
        vlan = eth_info.get("vlan", {})
        vlan_id = vlan.get("vlan-id", "Untagged") if isinstance(vlan, dict) else "Untagged"
        
        return sys_name, port_id, vlan_id
    except Exception:
        return "Searching...", "N/A", "N/A"

def update_display():
    epd = epd2in13b_V4.EPD()
    epd.init()
    
    # 2.13" v4 resolution is 250x122 (Landscape)
    width, height = epd.height, epd.width
    
    # Create blank monochrome image buffers (255 = white background)
    image_black = Image.new('1', (width, height), 255)
    image_red = Image.new('1', (width, height), 255)
    
    draw_black = ImageDraw.Draw(image_black)
    draw_red = ImageDraw.Draw(image_red)
    
    # Standard fonts
    font = ImageFont.load_default()

    # Network Telemetry
    eth0_ip = get_ip_address("eth0")
    netbird_ip = get_ip_address("wt0")
    switch_name, port_id, vlan = get_lldp_info()

    # Red Header Box
    draw_red.rectangle((0, 0, width, 18), fill=0)
    draw_black.text((6, 3), "BARNEY // FIELD APPLIANCE", font=font, fill=255)

    # Status Lines
    draw_black.text((6, 24),  f"ETH0 IP : {eth0_ip}", font=font, fill=0)
    draw_black.text((6, 38),  f"NetBird : {netbird_ip}", font=font, fill=0)
    draw_black.text((6, 52),  f"Switch  : {switch_name[:22]}", font=font, fill=0)
    draw_black.text((6, 66),  f"Port/V  : {port_id} (VLAN {vlan})", font=font, fill=0)

    # Serial Status Footer
    draw_red.line((0, 84, width, 84), fill=0)
    draw_black.text((6, 88), "Serial  : /dev/ttyCONSOLE (2001)", font=font, fill=0)

    # Send buffer to display
    epd.display(epd.getbuffer(image_black), epd.getbuffer(image_red))
    epd.sleep()

if __name__ == "__main__":
    update_display()
