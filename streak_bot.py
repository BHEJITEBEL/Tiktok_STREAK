import asyncio
import random
from playwright.async_api import async_playwright

# --- CONFIGURATION ---
COOKIE_PATH = "state.json" 
# 👇 Just put your friend's actual TikTok username here (keep the @ symbol)
FRIEND_USERNAME = "@hzeeqx"

async def send_streak():
    print("Starting bot...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = await browser.new_context(
            storage_state=COOKIE_PATH,
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # We add ?lang=en to force the page into English so the bot can read the "Message" button
        print(f"Navigating to {FRIEND_USERNAME}'s profile...")
        await page.goto(f"https://www.tiktok.com/{FRIEND_USERNAME}?lang=en")
        
        # 1. Click the "Message" button on their profile
        try:
            print("Looking for the Message button...")
            message_btn = page.locator('button:has-text("Message"), a:has-text("Message")').first
            await message_btn.wait_for(state="visible", timeout=15000)
            await message_btn.click()
            await asyncio.sleep(3) # Wait a few seconds for the chat window to open
        except Exception as e:
            print("Error: Could not find the Message button. Make sure you follow each other!")
            await browser.close()
            return
            
        # 2. Wait for the typing box to appear
        selector = 'div[contenteditable="true"]'
        try:
            await page.wait_for_selector(selector, timeout=20000)
            
            # Type a random streak message
            messages = ["🔥", "Streak!", "Daily 🔥", "Active ✨", "Streak"]
            chosen_msg = random.choice(messages)
            
            await page.fill(selector, chosen_msg)
            await asyncio.sleep(random.uniform(1, 3)) # Human-like pause before sending
            await page.keyboard.press("Enter")
            
            print(f"Successfully sent: {chosen_msg}")
        except Exception as e:
            print(f"Error: Could not type the message. {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(send_streak())
