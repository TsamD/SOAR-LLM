#!/usr/bin/env python3
import json
import time
import ipaddress
from datetime import datetime, timezone

dest_ip = "172.23.0.2"
SRC = "data/tpot/eve-tpot.json"
DST = "data/tpot/eve-tpot-replay.json"
LIMIT = 110

count = 0

with open(SRC, "r", encoding="utf-8") as src:
    with open(DST, "a", encoding="utf-8") as dst:
        for line in src:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("event_type") != "alert":
                continue

            src_ip = event.get("src_ip")
    #        dest_ip = event.get("dest_ip")
#	    dest_ip = "172.23.0.2"
            event["dest_ip"] = dest_ip
            signature = event.get("alert", {}).get("signature")

            if not src_ip or not dest_ip or not signature:
                continue

            try:
                ip = ipaddress.ip_address(src_ip)
            except ValueError:
                continue

            if not ip.is_global:
                continue

            event["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

            dst.write(json.dumps(event) + "\n")
            dst.flush()

            count += 1
            print(f"[+] replay alert {count}: {src_ip} -> {dest_ip} | {signature}")

            if count >= LIMIT:
                break

            time.sleep(1)
