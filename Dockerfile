FROM node:20-bullseye

# 1. Install System Deps (Run as Root)
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        curl \
        ca-certificates \
        fonts-liberation \
        libnss3 \
        libatk-bridge2.0-0 \
        libxkbcommon0 \
        libgtk-3-0 \
        libgbm1 \
        libasound2 \
        libxshmfence1 && \
    rm -rf /var/lib/apt/lists/*

# 2. Install n8n
RUN npm install -g n8n

# 3. Install Python Libraries
RUN pip3 install --no-cache-dir playwright playwright-stealth

# 4. Install Playwright OS Dependencies (Must be Root)
RUN playwright install-deps chromium

# 5. Create n8n user
RUN useradd -m n8n

# Switch to user 'n8n' BEFORE downloading the browser

USER n8n

# 6. Install Browser Binary (As 'n8n', so it goes to /home/n8n/.cache)
RUN playwright install chromium

# 7. Setup Scripts
WORKDIR /home/n8n/scripts
# Ensure we copy the file with the correct ownership
COPY --chown=n8n:n8n scraper.py .

EXPOSE 5678

CMD ["n8n"]