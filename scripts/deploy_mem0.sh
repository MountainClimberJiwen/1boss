#!/bin/bash
set -euo pipefail

REMOTE="root@150.158.27.27"
REMOTE_DIR="/opt/mem0"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)/services/mem0"

echo "==> Deploying mem0 service to ${REMOTE}"

# 1. Ensure remote directory exists
ssh -o ConnectTimeout=10 "${REMOTE}" "mkdir -p ${REMOTE_DIR} && mkdir -p /opt/mem0/data"

# 2. Sync server code
scp -o ConnectTimeout=10 \
  "${LOCAL_DIR}/main.py" \
  "${REMOTE}:${REMOTE_DIR}/main.py"

# 3. Install Python dependencies
ssh -o ConnectTimeout=10 "${REMOTE}" '
  set -e
  python3 -m ensurepip --upgrade 2>/dev/null || true
  python3 -m pip install -q fastapi "uvicorn[standard]>=0.23" mem0ai
'

# 4. Install /etc/mem0.env if not present
ssh -o ConnectTimeout=10 "${REMOTE}" '
  if [ ! -f /etc/mem0.env ]; then
    echo "OPENAI_API_KEY=" > /etc/mem0.env
    echo "MEM0_PORT=8000" >> /etc/mem0.env
    echo "MEM0_DATA_DIR=/opt/mem0/data" >> /etc/mem0.env
    echo "==> Created /etc/mem0.env (please edit and add OPENAI_API_KEY)"
  else
    echo "==> /etc/mem0.env already exists, leaving untouched"
  fi
'

# 5. Install systemd service
scp -o ConnectTimeout=10 \
  "${LOCAL_DIR}/mem0.service" \
  "${REMOTE}:/etc/systemd/system/mem0.service"

# 6. Reload daemon and (re)start service
ssh -o ConnectTimeout=10 "${REMOTE}" '
  systemctl daemon-reload
  systemctl enable mem0.service
  systemctl restart mem0.service
  sleep 2
  systemctl status mem0.service --no-pager || true
'

echo "==> Deployment complete"
echo "    Health:   http://${REMOTE/ root@/}:8000/health"
echo "    Docs:     http://${REMOTE/ root@/}:8000/docs"
echo "    Config:   /etc/mem0.env (set OPENAI_API_KEY for full functionality)"
