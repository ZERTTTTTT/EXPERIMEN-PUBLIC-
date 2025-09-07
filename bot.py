import time
import random
import logging
from threading import Thread, Lock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

lock = Lock()

# ---------- CONFIG ----------
NUM_THREADS = 5          # Jumlah thread / viewers bersamaan
STAY_TIME = 30           # Durasi stay di video (detik)
LOG_FILE = 'bot_log.txt'
# ----------------------------

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List User-Agent untuk stealth
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/119.0",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def create_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={get_random_user_agent()}")
    options.add_argument("--headless")  # Hapus jika ingin lihat browser
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1200,800")

    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver

def watch_video(url, stay_time=STAY_TIME):
    try:
        driver = create_driver()
        print(f"Opening video: {url}")
        driver.get(url)
        time.sleep(stay_time + random.uniform(0, 5))  # Simulate watching
        driver.quit()
        msg = f"Finished watching video: {url}"
        print(msg)
        logging.info(msg)
    except Exception as e:
        msg = f"Error watching video {url}: {e}"
        print(msg)
        logging.error(msg)

def worker(url, stay_time):
    while True:
        watch_video(url, stay_time)

def main():
    url = input("Enter TikTok or YouTube video URL: ").strip()
    global NUM_THREADS
    NUM_THREADS = int(input("Enter number of concurrent threads: ").strip())
    global STAY_TIME
    STAY_TIME = int(input("Enter approximate watch time per view (seconds): ").strip())

    threads = []
    for _ in range(NUM_THREADS):
        t = Thread(target=worker, args=(url, STAY_TIME))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
