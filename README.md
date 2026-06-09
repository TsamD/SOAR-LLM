# SOC-WAZUH-CALDERA-HIVE-CORTEX

Open-source SOC lab built with Docker Compose, combining attack simulation, detection, SIEM, incident response, automation, and notification.

![SOC Architecture](SOC.png)

---

## Overview

This project implements a complete SOC pipeline by separating each capability into functional components:

- attack simulation
- application layer (targets)
- detection
- SIEM
- incident response
- notification
- automation and AI enrichment

The architecture is designed to mimic a real SOC workflow from attack to response.

---

## Architecture by Function

###  Attack Simulation

- **MITRE CALDERA**
- Red team adversary emulation platform

Used to:
- simulate real attacks
- test SOC detection capabilities
- validate the security pipeline

Agent deployment:

```bash
scripts/deploy_caldera_agent.sh
````

Attack execution script:

```bash
scripts/Attacks
```

---

###  Applications Layer

* **server-app (Apache / vulnerable app)**
* **curl container**

Used as:

* attack targets
* traffic generators
* "zombie" host for CALDERA agent deployment

The CALDERA agent is deployed inside this environment.

---

###  Detection Layer

* **Suricata** → signature-based IDS
* **Zeek** → network traffic analysis
* **Wazuh Agent** → host monitoring

Used to:

* detect malicious activity
* generate alerts
* monitor both network and host behavior

---

###  SIEM Layer

* **Wazuh Stack**

  * wazuh.manager
  * wazuh.indexer
  * wazuh.dashboard

Used to:

* centralize logs
* correlate events
* generate alerts
* provide visibility through dashboards

---

###  Incident Response

* **TheHive**
* **Cortex**
* **Elasticsearch**
* **Cassandra**
* **Nginx**

Used to:

* manage alerts and cases
* enrich observables (IP, hash, etc.)
* perform automated analysis
* support incident investigation workflows

---

###  Notification Layer

* **Maildev**
* **Discord integration**

Used to:

* simulate email alerts
* send SOC notifications
* validate alerting mechanisms


---

##  Automation Workflow (n8n)

The following workflow illustrates the full SOC automation pipeline:


::contentReference[oaicite:0]{index=0}


>  Actual workflow used in this project: `workflow.png`

![SOC Workflow](./workflow.png)

###  Workflow Description

1. **Webhook (Wazuh → n8n)**
   - Receives alerts from Wazuh custom integration

2. **Fields Extraction**
   - Normalizes alert fields (rule, agent, IP, log)

3. **JavaScript Processing**
   - Formats data into a structured payload for LLM

4. **LLM Analysis (Ollama)**
   - Generates SOC-style summary:
     - Résumé
     - Criticité
     - Recommandation

5. **Create Alert (TheHive)**
   - Sends enriched alert

6. **Create Case**
   - Automatically opens investigation

7. **Observable Creation**
   - Adds IP / IOC to case

8. **Cortex Analyzer**
   - Runs enrichment (VirusTotal, AbuseIPDB, etc.)

9. **Notification**
   - Sends formatted alert to Discord

---

###  Notes

- The workflow must be imported from:
```

config/n8n/workflows/SOC.json

````

- You must configure:
- TheHive API key
- Cortex API key
- Ollama model (default: `qwen2.5:3b`)

- If the model is missing:
```bash
docker exec -it ollama ollama pull qwen2.5:3b
````

---

###  Why this matters

This workflow demonstrates:

* Full SOC automation chain
* AI-assisted alert triage
* Integration between SIEM, SOAR, and Threat Intelligence

```

---

## Stack Mapping

The project is deployed using multiple Docker Compose files:

* `docker-compose.yml`

  * applications
  * attack simulation
  * detection tools
  * mail system

* `docker-compose-wazuh.yml`

  * SIEM stack

* `docker-compose-thehive.yml`

  * incident response stack

* `docker-compose-n8n-ollama.yml`

  * automation and AI stack

---

## Summary

This lab provides a complete SOC workflow:

1. Attack simulation (CALDERA / scripts)
2. Detection (Suricata, Zeek, Wazuh agent)
3. SIEM correlation (Wazuh)
4. Automation (n8n)
5. AI enrichment (Ollama)
6. Incident creation (TheHive)
7. Analysis (Cortex)
8. Notification (Maildev / Discord)

---

## Goal

The objective of this project is not only to visualize logs, but to:

* build a full SOC pipeline
* automate incident handling
* test detection capabilities
* simulate realistic attack scenarios

```

---

##  Quick Start

This project is modular. Each component requires minimal configuration before use.

---

###  1. Start the Environment

Start the stacks (depending on your needs):

```bash
docker compose up -d
docker compose -f docker-compose-wazuh.yml up -d
docker compose -f docker-compose-thehive.yml up -d
docker compose -f docker-compose-n8n-ollama.yml up -d
````

---

###  2. Attack Simulation (CALDERA)

Deploy the CALDERA agent inside the target container:

```bash
scripts/deploy_caldera_agent.sh
```

Run attack scenarios:

```bash
scripts/Attacks
```

---

###  3. Incident Response (TheHive + Cortex)

Initialize the environment:

```bash
scripts/init.sh
```

  Important:

You MUST change default passwords (`changeme`) in:

* TheHive configuration
* Cortex configuration

---

###  4. SIEM (Wazuh)

Certificates are already provided, but you can generate your own:

```bash
tools/wazuh-certs-tool.sh
```

---

###  Import Wazuh Dashboard

Dashboard file:

```text
config/wazuh/wazuh_dashboard/SOC.ndjson
```

Import steps:

1. Go to **Wazuh Dashboard**
2. Navigate to:

   * *Dashboard Management* → *Saved Objects*
3. Click **Import**
4. Upload the `.ndjson` file

---

## Wazuh Integrations (n8n Webhook + Discord)

This project uses custom Wazuh integrations to:
- Send alerts to **n8n (webhook)**
- Send notifications to **Discord**

---

### 1. Enable Custom Integration Scripts

Enter the `wazuh.manager` container:

```bash
docker exec -it wazuh.manager bash
````

Then apply correct permissions:

```bash
chmod 750 /var/ossec/integrations/custom-*
chown root:wazuh /var/ossec/integrations/custom-*
```

---

### 2. Configure Discord Webhook

Edit the Wazuh manager configuration:

```text
config/wazuh/wazuh_cluster/wazuh_manager.conf
```

Locate the integration block and set your Discord webhook URL:

```xml
<integration>
  <name>custom-discord</name>
  <hook_url>https://discord.com/api/webhooks/XXXXX</hook_url>
  <alert_format>json</alert_format>
</integration>
```

---

### 3. Restart Wazuh Manager

Apply changes:

```bash
docker restart wazuh.manager
```

---

###  5. Automation (n8n)

Import workflow:

```text
config/n8n/workflows/SOC.json
```

After import:

* configure **TheHive API**
* configure **Cortex API**
* verify credentials

---

###  6. AI (Ollama)

Pull the required model:

```bash
docker exec -it <ollama_container> ollama pull qwen2.5:3b
```

If you use another model:

* update the **Ollama node** inside the n8n workflow

---

##  Important Notes

* Credentials are NOT exported → must be configured manually
* Some components are resource-intensive (Wazuh, TheHive, Elasticsearch)
* You can run stacks independently to reduce load

---

## Minimal Flow to Validate Setup

1. Deploy CALDERA agent
2. Run attack script
3. Observe detection in Wazuh
4. Check alert processing in n8n
5. Verify case creation in TheHive
6. Review enrichment in Cortex
7. Check notifications (Discord / Maildev)

---



