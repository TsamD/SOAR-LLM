FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apache2 \
    curl \
    vim \
    procps \
    gnupg \
    apt-transport-https \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# --- INSTALL WAZUH AGENT ---
RUN curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --dearmor -o /usr/share/keyrings/wazuh.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" \
    > /etc/apt/sources.list.d/wazuh.list && \
    apt-get update && \
    apt-get install -y wazuh-agent && \
    rm -rf /var/lib/apt/lists/*

# Page web
RUN echo '<html><body><h1>Victim OK</h1></body></html>' > /var/www/html/index.html

# --- CONFIG WAZUH AGENT ---
COPY ossec.conf /var/ossec/etc/ossec.conf

# --- START SCRIPT ---
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
