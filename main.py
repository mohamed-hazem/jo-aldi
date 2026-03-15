# Modules
from playwright.sync_api import Playwright, sync_playwright
from pathlib import Path
import time, re

from logs import setup_logger
# ===================================================================== #

# Login data
RUFNUMMER = "01633670473"
PASSWORT = "zamalkawy989"

class JoAldi:
    def __init__(self, playwright: Playwright):
        # Setup logger
        logs_dir = Path(__file__).parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        self.timestamp = time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime())
        log_file = logs_dir / f"{self.timestamp}.log"
        self.logger = setup_logger(str(log_file))
        
        # Init browser
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def _wait_for_page_load(self, timeout=5000):
        self.page.get_by_role("button", name="GB").wait_for(state="visible", timeout=timeout)

    def login(self):
        self.page.goto("https://www.alditalk-kundenportal.de/user/auth/account-overview/")
        self.page.get_by_test_id("uc-accept-all-button").click()
        self.page.get_by_role("textbox", name="Rufnummer").fill(RUFNUMMER)
        self.page.get_by_role("textbox", name="Passwort").fill(PASSWORT)
        self.page.locator(".checkbox-indicator").click()
        self.page.get_by_role("link", name="Anmelden", exact=True).click()

        # Wait for the page to load
        self._wait_for_page_load()

        self.logger.info("Logged in successfully.")

    def is_less_than_one_gb(self) -> bool:
        usage_text = self.page.locator("text=von 25 GB").locator("..").inner_text()
        match = re.search(r'Noch\s*(\d+(?:[.,]\d+)?)\s*([A-Za-z]+)\s*von', usage_text)
        
        if (match):
            number = float(match.group(1).replace(",", "."))
            unit = match.group(2)
            self.logger.info(f"Current data usage: {number} {unit}")

            if (unit == "GB" and number == 0) or (unit == "MB"):
                return True
        return False
    
    def add_one_gb(self):
        self.page.get_by_role("button", name="GB").click()
        self.logger.info("Added 1 GB of data.")
        
        time.sleep(1)
        self.page.reload()
        self._wait_for_page_load()

    def run(self):
        self.login()
        
        while True:
            if (self.is_less_than_one_gb()):
                self.add_one_gb()
            
            else:
                time.sleep(30)
                self.page.reload()
                self._wait_for_page_load()
            
# --------------------------------------------------------------------- #

def main(): 
    with sync_playwright() as playwright:
        j = JoAldi(playwright)
        j.run()

if (__name__ == "__main__"):
    main()
# --------------------------------------------------------------------- #