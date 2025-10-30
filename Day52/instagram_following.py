from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv()
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

SIMILIAR_ACCOUNT = "cars_show_123"
ID_INSTAGRAM = os.environ.get("ID")
PASS_INSTAGRAM = os.environ.get("PASS")
INSTAGRAM_URL = "https://www.instagram.com/"
INSTAGRAM_LOGIN = "https://www.instagram.com/accounts/login/"

class InstaFollower:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def login(self):
        self.driver.get(INSTAGRAM_LOGIN)
        wait = WebDriverWait(self.driver, timeout=5)
        try:
            allow_cookie = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'asz1')]")))
            allow_cookie.click()
            email_input = wait.until(lambda _: self.driver.find_element(By.NAME, value="username"))
            email_input.send_keys(ID_INSTAGRAM)
            password_input = wait.until(lambda _: self.driver.find_element(By.NAME, value ="password"))
            password_input.send_keys(PASS_INSTAGRAM)
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, '_aswp')]")))
            submit_button.click()
            login_info = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@role, 'button')]")))
            login_info.click()
        except "TimeoutException":
            print("⚠️ Timeout exceed.")
    def find_followers(self):
        wait = WebDriverWait(self.driver, timeout=100)
        try:
            search_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mount_0_0_OW"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[2]/span/div/a/div/div[2]/div/div/span/span')))
            search_click.click()
            input_search = wait.until(lambda _: self.driver.find_element(By.XPATH, value='//input[contains(@aria-label, "Search input")]'))
            input_search.send_keys()
            click_profile = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'html-div xdj266r')][1]")))
            click_profile.click()
        except "TimeoutException":
            print("⚠️ Timeout exceed.")

    def follow(self):
        follow_buttons = self.driver.find_elements(By.XPATH, "//button/div/div[text()='Follow']/ancestor::button")
        print(f"Found {len(follow_buttons)} users to follow.")
        for btn in follow_buttons:
            try:
                btn.click()
                print("👉 Followed one user.")
                time.sleep(random.uniform(2, 4))
            except:
                print("⚠️ Could not click follow button.")
                continue