# Start with the official n8n image
FROM docker.n8n.io/n8nio/n8n:latest

# Switch to root to install packages
USER root

# 1. Install Python, Pip, and system dependencies
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Playwright + stealth
RUN pip3 install --no-cache-dir playwright playwright-stealth

# 3. Install Chromium and required system deps
RUN playwright install chromium && \
    playwright install-deps chromium

# 4. Create the scripts folder and copy your scraper
WORKDIR /home/node/scripts
COPY scraper.py .

# 5. Fix permissions so n8n (node user) can run it
RUN chown -R node:node /home/node/scripts

# Switch back to the n8n user for security
USER node
