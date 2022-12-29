#!/usr/bin/env python3

from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import logging
from datetime import datetime
import smtplib
import sys
import os
from config import config
import time

logging.basicConfig(
    format = '%(levelname)s:%(message)s',
    level = logging.INFO,
    handlers = [
        logging.FileHandler('/tmp/out.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class Prenotami:
    def __init__(self, config: dict):
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument('--user-data-dir=/home/seluser/.config/google-chrome')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-setuid-sandbox')
        # options.binary_location = "/usr/bin/google-chrome"
        # self.driver = Chrome("/opt/selenium/chromedriver",options=chrome_options)
        self.driver = Chrome(options=chrome_options)
        self.config = config

    def login(self):

        try:
            self.driver.get('https://prenotami.esteri.it')
            time.sleep(2)
            self.driver.find_element(By.ID, 'login-email').send_keys(self.config['prenotami']['username'])
            self.driver.find_element(By.ID, 'login-password').send_keys(self.config['prenotami']['password'])
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            logging.info("Logged in to Prenotami.")

        except Exception as e:
            logging.info("TIMESTAMP: " + str(datetime.now()))
            logging.info("Failure to login occurred. Sending text notification...")
            logging.info("Exception: " + e)
            phone_numbers = [x for x in self.config['phone_numbers'] if x['dev']==True]
            [self.send_text(phone_number['number'],phone_number['carrier'],"Login to Pretonami failed, please check system.") for phone_number in phone_numbers]


    def check_appointments(self):

        try:
            self.driver.get('https://prenotami.esteri.it/Services')
            time.sleep(5)
            self.driver.find_element(By.XPATH, "//*[@id='dataTableServices']/tbody/tr[3]/td[4]/a/button").click()
            time.sleep(2)
            appts_available = self.driver.find_element(By.XPATH, "//*[@id='WlNotAvailable']").get_attribute("value")
            
            if appts_available == 'Al momento non ci sono date disponibili per il servizio richiesto':
                logging.info("TIMESTAMP: " + str(datetime.now()))
                logging.info("No change to prenotami detected.")
                sys.exit(0)
            else:
                message = "Change detected on prenotami, please check system for available appointments."
                phone_numbers = [x for x in self.config['phone_numbers']]
                [self.send_text(phone_number['number'], phone_number['carrier'], message) for phone_number in phone_numbers]
                logging.info("TIMESTAMP: " + str(datetime.now()))
                logging.info("Change detected on prenotami.")

        except Exception as e:
            message = "An exception occurred when attempting to check for apppointments on Prenotami, this may mean booking is available. \n {e}".format(e=e)
            phone_numbers = [x for x in self.config['phone_numbers']]
            [self.send_text(phone_number['number'], phone_number['carrier'], message) for phone_number in phone_numbers]
            logging.info("TIMESTAMP: " + str(datetime.now()))
            logging.info("Possible change detected on prenotami.")
            logging.info("Exception: " + str(e))

    def send_text(self, phone_number: str, carrier: str, message: str):

        try:
            recipient = phone_number + self.config['carriers'][carrier]
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.config['email']['username'], self.config['email']['password'])
            server.sendmail(self.config['email']['username'], recipient, message)

        except Exception as e:
            logging.info("TIMESTAMP: " + str(datetime.now()))
            logging.info("Failure to send text message.")
            logging.info("Exception: " + e)



