#!/bin/bash
# Barney Self-Updater Script
# Pulls latest code from GitHub and restarts Barney services

REPO_URL="https://github.com/alexp206/barney-barnacle.git"
INSTALL_DIR="/opt/barney"

echo "[INFO] Checking for Barney updates from ${REPO_URL}..."

if [ ! -d "${INSTALL_DIR}/.git" ]; then
    echo "[INFO] Initializing git repository at ${INSTALL_DIR}..."
    git clone --depth 1 "${REPO_URL}" "${INSTALL_DIR}_tmp"
    if [ -d "${INSTALL_DIR}_tmp" ]; then
        cp -r "${INSTALL_DIR}_tmp"/* "${INSTALL_DIR}/"
        cp -r "${INSTALL_DIR}_tmp"/.git "${INSTALL_DIR}/"
        rm -rf "${INSTALL_DIR}_tmp"
    fi
else
    cd "${INSTALL_DIR}" || exit 1
    git fetch origin main
    git reset --hard origin/main
fi

echo "[INFO] Updating Barney scripts and permissions..."
cp -f "${INSTALL_DIR}/barney-wifi.sh" /usr/local/bin/barney-wifi 2>/dev/null
chmod +x /usr/local/bin/barney-wifi 2>/dev/null
chmod +x "${INSTALL_DIR}"/*.py 2>/dev/null

echo "[INFO] Restarting Barney services..."
systemctl reset-failed barney-dashboard.service barney-led-status.service 2>/dev/null
systemctl restart barney-dashboard.service barney-led-status.service

echo "[SUCCESS] Barney successfully updated to latest version!"
