# Start with the official n8n image
FROM docker.n8n.io/n8nio/n8n:1-debian-bullseye

USER root

# Install Python + system deps
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Playwright + stealth
RUN pip3 install --no-cache-dir playwright playwright-stealth

# Install Chromium + required OS deps
RUN playwright install chromium && \
    playwright install-deps chromium

# Copy scraper
WORKDIR /home/node/scripts
COPY scraper.py .

RUN chown -R node:node /home/node/scripts

USER node
