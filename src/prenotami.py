from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
import sys
import time
import random


logging.basicConfig(
    format = '%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level = logging.INFO,
    handlers = [
        logging.FileHandler('/tmp/prenotami-bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)


def sleep(max_time: int):
    time.sleep(random.randint(1, max_time))


class PrenotamiBot:
    def __init__(self, config: dict, headless: bool = False):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--no-sandbox')

        if headless:
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--allow-running-insecure-content')
        # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        # chrome_options.add_argument(f'--user-agent="{user_agent}"')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--profile-directory=Default')
        # chrome_options.add_argument('--user-data-dir=/home/seluser/.config/google-chrome')
        # chrome_options.add_argument('--remote-debugging-port=9222')
        # chrome_options.add_argument('--disable-setuid-sandbox')
        # options.binary_location = "/usr/bin/google-chrome"
        # self.driver = Chrome("/opt/selenium/chromedriver",options=chrome_options)
        # self.driver = Chrome(options=chrome_options)
        self.driver = uc.Chrome(
            options=chrome_options,
            service=Service(ChromeDriverManager(version="114.0.5735.90").install(),
        ))
        self.config = config
        self.is_logged_in = False

    def login(self):
        try:
            self.driver.get("https://prenotami.esteri.it/")
            email_box = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "login-email"))
            )

            password_box = self.driver.find_element(By.ID, "login-password")
            email_box.send_keys(self.config['prenotami']['username'])
            password_box.send_keys(self.config['prenotami']['password'])
            sleep(4)
            button = self.driver.find_elements(
                By.XPATH, "//button[contains(@class,'button primary g-recaptcha')]"
            )
            self.driver.get_screenshot_as_file("screenshot-1.png")
            button[0].click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "logoutForm"))
            )
            logging.info("Logged in to Prenotami.")
            self.is_logged_in = True
        except Exception as e:
            self.driver.get_screenshot_as_file("prenotami-screenshot-login.png")
            logging.error(f"Failure to login occurred. Sending text notification. Exception: {e}")
            self._send_email("Login to Pretonami failed, please check system.")
            self.driver.quit()


    def check_appointments(self):
        if not self.is_logged_in:
            logging.info("Can't check for appointments: not logged in to Prenotami.")
            sys.exit(1)

        try:
            self.driver.get('https://prenotami.esteri.it/Services/Booking/287')
            time.sleep(5)
            try:
                appts_available = self.driver.find_element(By.XPATH,
                                                           "//*[@id='WlNotAvailable']"
                                                        ).get_attribute("value")
            except NoSuchElementException:
                message = "Change detected on Prenotami, please check system for available appointments."
                self.driver.get_screenshot_as_file("prenotami-screenshot-change.png")
                self._send_email(message)
                logging.info(message)
            else:
                logging.info(f"No dates available at the moment: {appts_available}")

        except Exception as e:
            self.driver.get_screenshot_as_file("prenotami-screenshot-appointment.png")
            message = f"An exception occurred when attempting book apppointments on Prenotami. This may mean booking is available.\n{e}"
            logging.error(f"Possible change detected on prenotami. Exception: {e}")
            self._send_email(message)
        finally:
            self.driver.quit()


    def _send_email(self, message: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender']
            msg['To'] = self.config['email']['recipient']
            msg['Subject'] = '[Prenotami-bot] notification'
            msg.attach(MIMEText(message, 'plain'))

            smtp = SMTP(self.config['email']['server'], 587)
            smtp.starttls()
            smtp.login(self.config['email']['username'], self.config['email']['password'])
            smtp.sendmail(self.config['email']['username'], self.config['email']['recipient'], msg.as_string())
            smtp.quit()
        except Exception as e:
            logging.error(f"Failure to send email. Exception: {e}")
