# Start with the official n8n image
FROM docker.n8n.io/n8nio/n8n:latest

# Switch to root to install packages
USER root

# 1. Install Python and Pip
RUN apk add --no-cache python3 py3-pip

# 2. Install Playwright and dependencies
# (We install Chromium specifically to save space)
RUN pip install playwright playwright-stealth
RUN playwright install chromium
RUN playwright install-deps chromium

# 3. Create the scripts folder and copy your scraper
WORKDIR /home/node/scripts
COPY scraper.py .

# 4. Fix permissions so n8n (node user) can run it
RUN chown -R node:node /home/node/scripts

# Switch back to the n8n user for security
USER node