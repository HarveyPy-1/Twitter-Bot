from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

PROMISED_DOWN = 200
PROMISED_UP = 50
TWITTER_EMAIL = "emazonconsult@gmail.com"
TWITTER_PASSWORD = "VerySecurePassword"
TWITTER_USERNAME = "speed_test_py"


class InternetSpeedTwitterBot():
    def __init__(self, driver_path):
        self.down = 0
        self.up = 0
        chrome_driver = Service(driver_path)
        self.driver = webdriver.Chrome(service=chrome_driver)

    def get_internet_speed(self):
        self.driver.get("https://www.fast.com")
        time.sleep(30)
        # You can try to use a exception handler here and try to check upload speed constantly in a while loop
        # until there's no error, then the while loop breaks. Instead of using time.sleep()
        check_upload_speed = self.driver.find_element(By.ID, "show-more-details-link")
        check_upload_speed.click()

        self.down_speed = self.driver.find_element(By.ID, "speed-value")
        self.up_speed = self.driver.find_element(By.ID, "upload-value")

        return self.down_speed.text, self.up_speed.text

    def tweet_at_provider(self):
        down, up = self.get_internet_speed()
        self.driver.get("https://twitter.com/i/flow/login")

        time.sleep(5)

        login_input = self.driver.find_element(By.CSS_SELECTOR, "div input")
        login_input.click()
        login_input.send_keys(TWITTER_EMAIL)
        login_input.send_keys(Keys.ENTER)

        time.sleep(2)

        bot_check = True
        while bot_check:
            try:
                password_input = self.driver.find_element(By.NAME, "password")
                password_input.click()
                password_input.send_keys(TWITTER_PASSWORD)
                password_input.send_keys(Keys.ENTER)
                bot_check = False
            except NoSuchElementException:
                username_input = self.driver.find_element(By.CSS_SELECTOR, "div input")
                username_input.send_keys(TWITTER_USERNAME)
                username_input.send_keys(Keys.ENTER)
                time.sleep(2)

        time.sleep(5)

        if int(down) < 140 or int(up) < 40:
            tweet_field = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
            tweet_field.click()
            tweet_field.send_keys(f"Hey Internet Provider, why is my internet speed {down}mbps down/{up}mbps up, when I pay for {PROMISED_DOWN}mbps down/{PROMISED_UP}mbps up?")

            tweet_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
            tweet_button.click()
        else:
            print(f"Your internet speed is {down}mbps down and {up}mbps up.")
