from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ACCOUNT_EMAIL = "fulger@test.com"
ACCOUNT_PASSWORD = "Logitech123"
GYM_URL = "https://appbrewery.github.io/gym/"

class SeleniunConfigure:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        self.chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(GYM_URL)

    def login(self):
        wait = WebDriverWait(self.driver, timeout=5)
        logging_button = wait.until(lambda _: self.driver.find_element(By.ID, value = "login-button"))
        logging_button.click()
        email_input = wait.until(lambda _: self.driver.find_element(By.ID, value = "email-input"))
        email_input.send_keys(ACCOUNT_EMAIL)
        password_input = wait.until(lambda _: self.driver.find_element(By.ID, value = "password-input"))
        password_input.send_keys(ACCOUNT_PASSWORD)
        press_login = wait.until(lambda _: self.driver.find_element(By.ID, value="submit-button"))
        press_login.click()

    def book_upcoming_tuesday(self):
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id^='day-group-']")))
        all_groups = self.driver.find_elements(By.CSS_SELECTOR, value="div[id^='day-group-']")
        for card in all_groups:
            day_title = card.find_element(By.CSS_SELECTOR, value = "h2[id^='day-title-']").text
            if "Tue" in day_title:
                time_tue = card.find_elements(By.CSS_SELECTOR, value = "p[id^='class-time-']")
                for t in time_tue:
                    if "6:00 PM" in t.text:
                        click_button = card.find_element(By.CSS_SELECTOR, value = "button[id^='book-button-']")
                        click_button.click()
                        print(f"✓ Booked for {day_title} and at hour {t.text}")
        #Just for debug
        # see_booking = self.driver.find_element(By.ID, value="my-bookings-link")
        # see_booking.click()




