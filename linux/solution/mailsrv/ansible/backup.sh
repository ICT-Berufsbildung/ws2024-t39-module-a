#!/bin/bash

# Define source directories
MAILBOX_DIR="/var/mailboxes"
DOVECOT_CONFIG_DIR="/etc/dovecot"
POSTFIX_CONFIG_DIR="/etc/postfix"

# Define target directory
BACKUP_DIR="/opt/backup"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup mail data using rsync with versioning
rsync -av --delete --backup --backup-dir="$BACKUP_DIR/$(date +%Y-%m-%d_%H-%M-%S)" --suffix="_$(date +%Y-%m-%d_%H-%M-%S)" $MAILBOX_DIR $BACKUP_DIR/mailboxes

# Backup Dovecot config files with versioning
rsync -av --backup --backup-dir="$BACKUP_DIR/$(date +%Y-%m-%d_%H-%M-%S)" --suffix="_$(date +%Y-%m-%d_%H-%M-%S)" $DOVECOT_CONFIG_DIR $BACKUP_DIR/dovecot

# Backup Postfix config files with versioning
rsync -av --backup --backup-dir="$BACKUP_DIR/$(date +%Y-%m-%d_%H-%M-%S)" --suffix="_$(date +%Y-%m-%d_%H-%M-%S)" $POSTFIX_CONFIG_DIR $BACKUP_DIR/postfix

# Print completion message
echo "Backup completed successfully."