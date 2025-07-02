#!/bin/bash
tail -Fn0 /var/log/kern.log | \
while read line ; do
    echo "$line" | grep "SYN_SCAN" &> /dev/null
    if [ $? = 0 ]
    then
        echo "[!] Wykryto skanowanie SYN - $(date)" >> /var/log/scan_detected.log
    fi
done