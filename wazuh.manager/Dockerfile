FROM wazuh/wazuh-manager:4.14.1

USER root

RUN /var/ossec/framework/python/bin/python3 -m ensurepip || true && \
    /var/ossec/framework/python/bin/python3 -m pip install --no-cache-dir requests
