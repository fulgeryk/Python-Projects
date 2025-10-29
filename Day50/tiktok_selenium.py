from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv()
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TIKTOK_URL = "https://www.tiktok.com/"
FB_ID = os.environ.get("FACEBOOK_ID")
FB_PASS = os.environ.get("FACEBOOK_PASSWORD")

class SeleniumTikTok:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(TIKTOK_URL)


    def close_toast(self):
        wait = WebDriverWait(self.driver, timeout=5)
        try:
            close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close toast']")))
            close_btn.click()
            print("✅ Closed toast notification.")
        except "TimeoutException":
            print("⚠️ No toast popup detected.")

    def login(self):
        wait = WebDriverWait(self.driver, timeout=5)
        try:
            print(self.driver.window_handles)
            login_btn = wait.until(EC.element_to_be_clickable((By.ID, "top-right-action-bar-login-button")))
            login_btn.click()
            facebook_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[1]/div/div/div[3]/div[2]')))
            facebook_btn.click()
            time.sleep(2)
            windows = self.driver.window_handles
            #new_page
            self.driver.switch_to.window(windows[-1])
            print("Current window:", self.driver.current_window_handle)
            allow_cookies_facebook = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="facebook"]/body/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div/span/span')))
            allow_cookies_facebook.click()
            email_input =  wait.until(lambda _: self.driver.find_element(By.XPATH, value ='//*[@id="email"]'))
            email_input.send_keys(FB_ID)
            password_input = wait.until(lambda _: self.driver.find_element(By.XPATH, value ='//*[@id="pass"]'))
            password_input.send_keys(FB_PASS)
            login_button = wait.until(lambda _: self.driver.find_element(By.NAME, value ='login'))
            login_button.click()
        except:
            print("⚠️ LOGGING BUTTON NOT FOUND")

    def go_to_home(self):
        time.sleep(20)
        wait = WebDriverWait(self.driver, timeout=5)
        try:
            home_button = wait.until(lambda _: self.driver.find_element(By.XPATH, value='//*[@id="app"]/div[2]/div[1]/div/div[3]/div[1]/h2[1]/div/a/button'))
            home_button.click()
        except:
            print("Home button not found")

    def scroll(self):
        time.sleep(10)
        wait = WebDriverWait(self.driver, timeout=5)
        try:
            scroll_button = wait.until(lambda _: self.driver.find_element(By.XPATH, value='//*[@id="main-content-homepage_hot"]/aside/div/div[2]/button'))
            scroll_button.click()
        except:
            print("Scroll Button not found")