#!/bin/bash
# Barney Self-Updater Script
INSTALL_DIR="/opt/barney"

echo "[INFO] Updating Barney from GitHub..."
if [ ! -d "${INSTALL_DIR}/.git" ]; then
    echo "[INFO] Initializing git repository at ${INSTALL_DIR}..."
    git clone --depth 1 https://github.com/alexp206/barney-barnacle.git "${INSTALL_DIR}_tmp"
    if [ -d "${INSTALL_DIR}_tmp" ]; then
        cp -r "${INSTALL_DIR}_tmp"/* "${INSTALL_DIR}/"
        cp -r "${INSTALL_DIR}_tmp"/.git "${INSTALL_DIR}/"
        rm -rf "${INSTALL_DIR}_tmp"
    fi
else
    cd "${INSTALL_DIR}" || exit 1
    git fetch origin main &>/dev/null
    git reset --hard origin/main &>/dev/null
fi

echo "[INFO] Updating Barney scripts and permissions..."
cp -f "${INSTALL_DIR}/barney-wifi.sh" /usr/local/bin/barney-wifi 2>/dev/null
chmod +x /usr/local/bin/barney-wifi 2>/dev/null
chmod +x "${INSTALL_DIR}"/*.py 2>/dev/null

echo "[INFO] Scheduling service restart..."
(sleep 1 && systemctl reset-failed barney-dashboard.service barney-led-status.service && systemctl restart barney-dashboard.service barney-led-status.service) &

echo "[SUCCESS] Update process initiated!"
