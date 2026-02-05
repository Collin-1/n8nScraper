import sys
import asyncio
import json
import random
from playwright.async_api import async_playwright

# use manual flags in the browser launch options instead.

async def scrape(url):
    async with async_playwright() as p:
        # Launch Chrome with Manual Stealth Flags
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled", # <--- Anti-Bot flag
                "--no-sandbox", 
                "--disable-setuid-sandbox"
            ]
        )
        
        # Create a context with a realistic User Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        
        try:
            # Go to the URL (timeout after 60 seconds)
            await page.goto(url, timeout=60000)
            
            # Random "Human" pause
            await page.wait_for_timeout(random.randint(1000, 3000))
            
            # Get the content
            content = await page.content()
            
            # Print success JSON
            print(json.dumps({"status": "success", "html": content}))
            
        except Exception as e:
            # Print error JSON
            print(json.dumps({"status": "error", "message": str(e)}))
        finally:
            await browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(scrape(sys.argv[1]))
    else:
        print(json.dumps({"status": "error", "message": "No URL provided"}))