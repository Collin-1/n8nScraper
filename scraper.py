import sys
import asyncio
import json
import random
import argparse
from playwright.async_api import async_playwright

# Parse arguments cleanly
parser = argparse.ArgumentParser()
parser.add_argument("url", help="The starting URL")
parser.add_argument("--selector", help="CSS selector for the 'Next' button", default=None)
parser.add_argument("--max", help="Max pages to scrape", type=int, default=1)
args = parser.parse_args()

async def scrape():
    async with async_playwright() as p:
        # Launch options
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        collected_html = []
        
        try:
            # 1. Go to the first page
            print(f"Visiting: {args.url}", file=sys.stderr)
            await page.goto(args.url, timeout=60000)
            await page.wait_for_timeout(random.randint(1000, 3000))
            
            # Loop for pagination
            page_count = 0
            while page_count < args.max:
                # Store current page HTML
                content = await page.content()
                collected_html.append(content)
                page_count += 1
                
                # Stop if we reached the limit
                if page_count >= args.max:
                    break
                
                # Stop if no selector was provided (Single page mode)
                if not args.selector:
                    break

                # 2. Try to find and click the "Next" button
                next_button = page.locator(args.selector)
                
                if await next_button.count() > 0 and await next_button.is_visible():
                    print(f"Clicking Next (Page {page_count + 1})...", file=sys.stderr)
                    
                    # Click and wait for navigation
                    await asyncio.gather(
                        page.click(args.selector),
                        page.wait_for_load_state("domcontentloaded") # Wait for page load
                    )
                    
                    # Human pause
                    await page.wait_for_timeout(random.randint(2000, 4000))
                else:
                    print("No 'Next' button found. Stopping.", file=sys.stderr)
                    break

            # Output ALL pages as a JSON list
            print(json.dumps({"status": "success", "pages": collected_html}))

        except Exception as e:
            print(json.dumps({"status": "error", "message": str(e)}))
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape())