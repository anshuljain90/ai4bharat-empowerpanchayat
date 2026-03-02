#!/bin/bash
# =============================================================
# eGramSabha — MongoDB Backup Setup
# =============================================================
# Run once to configure daily automated MongoDB backups.
# Usage: bash scripts/setup-backups.sh
# =============================================================

set -e

BACKUP_DIR=~/backups
SCRIPT_PATH=~/backup-mongodb.sh

echo "========================================="
echo "  Setting Up MongoDB Backups"
echo "========================================="

# --- 1. Create backup directory ---
mkdir -p "$BACKUP_DIR"

# --- 2. Create backup script ---
cat > "$SCRIPT_PATH" << 'BACKUPEOF'
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups
CONTAINER_NAME=$(docker ps -qf "name=mongodb")

if [ -z "$CONTAINER_NAME" ]; then
    echo "$(date): ERROR - MongoDB container is not running!"
    exit 1
fi

echo "$(date): Starting MongoDB backup: $TIMESTAMP"

# Run mongodump inside the container
docker exec "$CONTAINER_NAME" mongodump --out "/tmp/backup_${TIMESTAMP}" --quiet

# Copy from container to host
docker cp "$CONTAINER_NAME:/tmp/backup_${TIMESTAMP}" "${BACKUP_DIR}/backup_${TIMESTAMP}"

# Clean up inside container
docker exec "$CONTAINER_NAME" rm -rf "/tmp/backup_${TIMESTAMP}"

# Compress the backup
cd "$BACKUP_DIR"
tar -czf "backup_${TIMESTAMP}.tar.gz" "backup_${TIMESTAMP}"
rm -rf "backup_${TIMESTAMP}"

# Remove backups older than 7 days
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

BACKUP_SIZE=$(du -sh "${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz" | cut -f1)
echo "$(date): Backup completed: backup_${TIMESTAMP}.tar.gz (${BACKUP_SIZE})"
BACKUPEOF

chmod +x "$SCRIPT_PATH"

# --- 3. Run initial backup ---
echo ""
echo "Running initial backup..."
bash "$SCRIPT_PATH"

# --- 4. Setup cron job ---
echo ""
echo "Adding daily backup cron job (runs at 2 AM)..."

# Add cron entry (avoid duplicates)
CRON_ENTRY="0 2 * * * $SCRIPT_PATH >> $BACKUP_DIR/backup.log 2>&1"
(crontab -l 2>/dev/null | grep -v "backup-mongodb" ; echo "$CRON_ENTRY") | crontab -

echo ""
echo "========================================="
echo "  Backup Setup Complete!"
echo "========================================="
echo ""
echo "Backups stored in: $BACKUP_DIR"
echo "Cron schedule: Daily at 2:00 AM"
echo "Retention: 7 days"
echo ""
echo "Manual backup: bash ~/backup-mongodb.sh"
echo "View backup log: tail -f ~/backups/backup.log"
echo ""
echo "To restore from a backup:"
echo "  1. tar -xzf ~/backups/backup_XXXXXXXX_XXXXXX.tar.gz"
echo "  2. docker cp backup_XXXXXXXX_XXXXXX \$(docker ps -qf name=mongodb):/tmp/restore"
echo "  3. docker exec \$(docker ps -qf name=mongodb) mongorestore /tmp/restore"
echo "========================================="
