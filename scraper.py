import sys
import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth.stealth import stealth_async

async def scrape(url):
    async with async_playwright() as p:
        # Launch options that help avoid detection
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled", # Hides "navigator.webdriver" flag
                "--no-sandbox", 
                "--disable-dev-shm-usage"
            ]
        )
        
        # Create a context with a realistic User Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        
        # APPLY STEALTH: This injects JS to fake plugins, languages, and permissions
        await stealth_async(page)
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Human-like delay (randomized between 2-5 seconds)
            await page.wait_for_timeout(random.randint(2000, 5000))
            
            # Extract content
            content = await page.content()
            
            # Print content to stdout so n8n can capture it
            print(content) 
            
        except Exception as e:
            # Handle errors gracefully so n8n doesn't crash hard
            print(f"Error: {e}", file=sys.stderr)
        finally:
            await browser.close()

if __name__ == "__main__":
    # Get the URL from the command line argument passed by n8n
    target_url = sys.argv[1] 
    asyncio.run(scrape(target_url))