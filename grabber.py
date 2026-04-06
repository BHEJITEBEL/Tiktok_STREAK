import customtkinter as ctk
from playwright.sync_api import sync_playwright
from github import Github, Auth
import os

# --- YOUR CONFIGURATION ---
GITHUB_TOKEN = "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"  # Put the token you just made here
REPO_NAME = "BHEJITEBEL/Tiktok_STREAK" # e.g. "johndoe/streak-bot"

def upload_to_github(file_path):
    try:
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        
        with open(file_path, "r") as f:
            content = f.read()
        
        # This updates the file if it exists, or creates it if it doesn't
        try:
            contents = repo.get_contents("state.json")
            repo.update_file("state.json", "Update cookies", content, contents.sha)
        except:
            repo.create_file("state.json", "Initial cookie upload", content)
        
        return True
    except Exception as e:
        print(f"GitHub Error: {e}")
        return False

def start_process():
    status_label.configure(text="Opening TikTok...", text_color="yellow")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tiktok.com/login")
        
        # UI instructions
        info_label.configure(text="1. Log in to TikTok.\n2. Once your feed loads, CLOSE this browser.")
        
        # Wait for user to close browser
        while len(browser.contexts) > 0:
            context.storage_state(path="state.json")
            page.wait_for_timeout(1000)

    # Browser is closed, now upload
    status_label.configure(text="Uploading to Cloud...", text_color="cyan")
    if upload_to_github("state.json"):
        status_label.configure(text="DONE! You can close this app now.", text_color="green")
        info_label.configure(text="The streak will start automatically in the cloud.")
    else:
        status_label.configure(text="Upload Failed. Check Token/Repo.", text_color="red")

# --- UI Setup ---
app = ctk.CTk()
app.title("Streak Setup")
app.geometry("400x300")

ctk.CTkLabel(app, text="TikTok Streak Setup", font=("Arial", 20)).pack(pady=20)
info_label = ctk.CTkLabel(app, text="Click below to start.", wraplength=300)
info_label.pack(pady=10)

btn = ctk.CTkButton(app, text="Connect TikTok", command=start_process, fg_color="#FE2C55")
btn.pack(pady=20)

status_label = ctk.CTkLabel(app, text="Ready", text_color="gray")
status_label.pack(pady=10)

app.mainloop()