touch /data/$LOG_PATH
tail -f /data/$LOG_PATH &
crond -f