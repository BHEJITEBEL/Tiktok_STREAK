import asyncio
import random
from playwright.async_api import async_playwright

# --- CONFIG ---
# The EXE will upload 'state.json' to the same folder as this script in the repo
COOKIE_PATH = "state.json" 
# Replace this with the link to the TikTok chat (get it from your browser)
TARGET_URL = "https://www.tiktok.com/messages?lang=en&u=YOUR_FRIEND_ID"

async def send_streak():
    async with async_playwright() as p:
        # Launching headless=True because there is no screen in the cloud
        browser = await p.chromium.launch(headless=True)
        
        # Load the cookies the user uploaded via the EXE
        context = await browser.new_context(storage_state=COOKIE_PATH)
        page = await context.new_page()
        
        print("Navigating to chat...")
        await page.goto(TARGET_URL)
        
        # Wait for the message box to be interactable
        # TikTok's message box is usually a div with contenteditable="true"
        selector = 'div[contenteditable="true"]'
        try:
            await page.wait_for_selector(selector, timeout=15000)
            
            # Type a random streak message
            messages = ["🔥", "APIII", "api 🔥", "Streak"]
            chosen_msg = random.choice(messages)
            
            await page.fill(selector, chosen_msg)
            await asyncio.sleep(random.uniform(1, 3)) # Human-like pause
            await page.keyboard.press("Enter")
            
            print(f"Successfully sent: {chosen_msg}")
        except Exception as e:
            print(f"Failed to find message box: {e}")
            # Take a screenshot if it fails so you can see why in GitHub logs
            await page.screenshot(path="error_screenshot.png")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(send_streak())
