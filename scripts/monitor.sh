#!/bin/bash
# =============================================================
# eGramSabha — Health Check / Monitoring Script
# =============================================================
# Usage: bash scripts/monitor.sh
# Add to cron for automatic monitoring:
#   */5 * * * * /home/ec2-user/ai4bharat-empowerpanchayat/scripts/monitor.sh >> ~/logs/monitor.log 2>&1
# =============================================================

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ALERT=false

echo "--- Health Check: $(date) ---"

# --- Check each container ---
SERVICES=("frontend" "backend" "video-mom-backend" "mongodb")
for SERVICE in "${SERVICES[@]}"; do
    CONTAINER=$(docker ps -qf "name=${SERVICE}" 2>/dev/null)
    if [ -z "$CONTAINER" ]; then
        echo "ALERT: $SERVICE is NOT running!"
        ALERT=true
    else
        STATUS=$(docker inspect --format='{{.State.Status}}' "$CONTAINER" 2>/dev/null)
        echo "OK: $SERVICE ($STATUS)"
    fi
done

# --- Check disk usage ---
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "WARNING: Disk usage is at ${DISK_USAGE}%"
    ALERT=true
else
    echo "OK: Disk usage at ${DISK_USAGE}%"
fi

# --- Check memory ---
FREE_MEM=$(free -m | awk '/^Mem:/{print $7}')
TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
if [ "$FREE_MEM" -lt 150 ]; then
    echo "WARNING: Low available memory: ${FREE_MEM}MB / ${TOTAL_MEM}MB"
    ALERT=true
else
    echo "OK: Memory available: ${FREE_MEM}MB / ${TOTAL_MEM}MB"
fi

# --- Check swap ---
SWAP_USED=$(free -m | awk '/^Swap:/{print $3}')
SWAP_TOTAL=$(free -m | awk '/^Swap:/{print $2}')
if [ "$SWAP_TOTAL" -gt 0 ] && [ "$SWAP_USED" -gt 0 ]; then
    echo "INFO: Swap usage: ${SWAP_USED}MB / ${SWAP_TOTAL}MB"
fi

# --- Test HTTP endpoint ---
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "OK: Frontend responding (HTTP $HTTP_CODE)"
else
    echo "ALERT: Frontend not responding (HTTP $HTTP_CODE)"
    ALERT=true
fi

# --- Summary ---
if [ "$ALERT" = true ]; then
    echo "STATUS: ISSUES DETECTED"
else
    echo "STATUS: ALL OK"
fi
echo ""
