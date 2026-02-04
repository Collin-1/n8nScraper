FROM node:20-bullseye

# Install system deps
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

# Install n8n
RUN npm install -g n8n

# Install Playwright
RUN pip3 install --no-cache-dir playwright playwright-stealth
RUN playwright install chromium && playwright install-deps chromium

# Create n8n user
RUN useradd -m n8n
USER n8n

# Copy scraper
WORKDIR /home/n8n/scripts
COPY scraper.py .

EXPOSE 5678

CMD ["n8n"]
