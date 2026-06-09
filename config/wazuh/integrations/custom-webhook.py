#!/usr/bin/env python3
import json
import sys
import urllib.request

alert_file = sys.argv[1]
hook_url = sys.argv[3]

with open(alert_file, 'r', encoding='utf-8') as f:
    alert = json.load(f)

rule = alert.get("rule", {}) or {}
agent = alert.get("agent", {}) or {}
data_field = alert.get("data", {}) or {}
alert_data = data_field.get("alert", {}) or {}
metadata = alert_data.get("metadata", {}) or {}
mitre = rule.get("mitre", {}) or {}

rule_id = str(rule.get("id", ""))


if rule_id in ["20101", "86601"]:
    sys.exit(0)

payload = {
    "full_log": alert.get("full_log", ""),
    "rule_id": rule.get("id"),
    "rule_description": rule.get("description"),

    "agent_name": agent.get("name", "agentless" if "agentless" in alert else ""),
    "agent_id": agent.get("id", ""),
    "src_ip": data_field.get("src_ip") or data_field.get("srcip") or alert.get("srcip") or "",
    "cve": metadata.get("cve", "N/A"),
    "mitre": {
        "id": mitre.get("id", []),
        "tactic": mitre.get("tactic", []),
        "technique": mitre.get("technique", []),
    },
    "raw": alert
}

data = json.dumps(payload).encode("utf-8")

req = urllib.request.Request(
    hook_url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req, timeout=10) as response:
    response.read()
