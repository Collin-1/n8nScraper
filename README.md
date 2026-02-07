# n8nScraper

Automated HTML scraper designed to run inside an n8n workflow or as a standalone CLI utility. The script uses Playwright with Chromium, manual anti-bot flags, and pagination support so you can capture content from multi-page flows.

## Features
- Headless Chromium scraping with Playwright async API
- Optional pagination by clicking a Next button located via CSS selector
- JSON-formatted stdout for easy consumption by n8n workflows or other tooling
- Docker image that bundles n8n, Python, Playwright, and required system dependencies

## Requirements
- Python 3.10+
- playwright and playwright-stealth
- Chromium browser binaries installed via playwright install chromium

## Local Setup
`
python -m venv venv
venv\Scripts\activate          # Windows
pip install playwright playwright-stealth
playwright install chromium
`

## CLI Usage
`
python scraper.py <url> [--selector ".next-button"] [--max 5]
`
- url: Starting page to load (required)
- --selector: CSS selector for the button or link that advances to the next page (optional)
- --max: Upper bound on the number of pages to capture (default: 1)

The script emits JSON on stdout. Example success payload:
`
{"status": "success", "pages": ["<html>...</html>", "<html>...</html>"]}
`

Errors include a message field describing the failure:
`
{"status": "error", "message": "Timeout 60000ms exceeded."}
`

## Integrating with n8n
1. Deploy the Docker image built from the included Dockerfile (see below).
2. Mount or copy scraper.py into the container if you customize it.
3. Configure an n8n Execute Command node to run the script and parse the returned JSON.

## Docker Image
The provided Dockerfile extends node:20-bullseye, installs n8n globally, sets up Playwright with its OS-level dependencies, and copies scraper.py into /home/n8n/scripts under the non-root n8n user.

Build the image:
`
docker build -t n8n-scraper .
`

Run n8n with the bundled scraper script:
`
docker run -p 5678:5678 n8n-scraper
`

## Troubleshooting
- Ensure Chromium binaries are installed (playwright install chromium).
- Increase --max gradually; some sites detect rapid pagination.
- Use --selector that uniquely matches the Next button; ambiguous selectors can cause click failures.
- Check stderr logs for progress messages when diagnosing pagination issues.

## License
MIT
