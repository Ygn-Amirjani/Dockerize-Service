#!/bin/bash

CONFIG_PATH=/root/.s3cfg
MOUNT_POINT={{ backup_path }}
BUCKET_NAME={{ s3_sandoghche }}

find $MOUNT_POINT -type f -mtime +5 -delete
s3cmd -c $CONFIG_PATH sync $MOUNT_POINT --preserve --delete-removed s3://$BUCKET_NAME
