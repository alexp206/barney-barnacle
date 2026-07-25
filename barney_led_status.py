#!/usr/bin/env python3
import time
import os
import subprocess

def find_led_path(name):
    for candidate in [f"/sys/class/leds/{name}", f"/sys/class/leds/led0" if name == "ACT" else "/sys/class/leds/led1"]:
        if os.path.exists(candidate):
            return candidate
    return None

act_led = find_led_path("ACT")
pwr_led = find_led_path("PWR")

def set_led_trigger(led_path, trigger):
    if not led_path:
        return
    trig_file = os.path.join(led_path, "trigger")
    if os.path.exists(trig_file):
        try:
            with open(trig_file, "w") as f:
                f.write(trigger)
        except Exception:
            pass

def check_netbird_vpn():
    try:
        out = subprocess.check_output(["netbird", "status"], stderr=subprocess.DEVNULL).decode("utf-8")
        return "Connected" in out
    except Exception:
        return False

def check_network_connectivity():
    try:
        res = subprocess.call(["ping", "-c", "1", "-W", "2", "1.1.1.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res == 0
    except Exception:
        return False

def main():
    while True:
        vpn_ok = check_netbird_vpn()
        net_ok = check_network_connectivity()

        # Green ACT LED: Heartbeat when NetBird VPN is Connected, None when down
        if vpn_ok:
            set_led_trigger(act_led, "heartbeat")
        else:
            set_led_trigger(act_led, "none")

        # Red PWR LED: Solid ON when internet OK, Rapid Flash (timer) on network failure
        if net_ok:
            set_led_trigger(pwr_led, "default-on")
        else:
            set_led_trigger(pwr_led, "timer")
            if pwr_led:
                on_file = os.path.join(pwr_led, "delay_on")
                off_file = os.path.join(pwr_led, "delay_off")
                if os.path.exists(on_file):
                    try:
                        with open(on_file, "w") as f: f.write("200")
                        with open(off_file, "w") as f: f.write("200")
                    except Exception: pass

        time.sleep(5)

if __name__ == "__main__":
    main()
