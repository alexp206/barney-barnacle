#!/bin/bash
# Barney Update Status Checker
INSTALL_DIR="/opt/barney"
STATUS_FILE="/tmp/barney_update_status.json"

git config --global --add safe.directory /opt/barney 2>/dev/null

if [ ! -d "${INSTALL_DIR}/.git" ]; then
    echo '{"status": "not_git_repo", "message": "Barney is not running from a git clone"}' > "${STATUS_FILE}"
    exit 0
fi

cd "${INSTALL_DIR}" || exit 1
git -c safe.directory=/opt/barney fetch origin main &>/dev/null
LOCAL_COMMIT=$(git -c safe.directory=/opt/barney rev-parse --short HEAD 2>/dev/null)
REMOTE_COMMIT=$(git -c safe.directory=/opt/barney rev-parse --short origin/main 2>/dev/null)

if [ "${LOCAL_COMMIT}" = "${REMOTE_COMMIT}" ]; then
    echo "{\"status\": \"up_to_date\", \"local_commit\": \"${LOCAL_COMMIT}\", \"remote_commit\": \"${REMOTE_COMMIT}\"}" > "${STATUS_FILE}"
else
    echo "{\"status\": \"update_available\", \"local_commit\": \"${LOCAL_COMMIT}\", \"remote_commit\": \"${REMOTE_COMMIT}\"}" > "${STATUS_FILE}"
fi
