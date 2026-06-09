#!/bin/bash

# Start wazuh agent
/var/ossec/bin/wazuh-control start

# Start apache
apache2ctl -D FOREGROUND
