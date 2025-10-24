from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv()
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ACCOUNT_EMAIL = os.environ.get("EMAIL")
ACCOUNT_PASSWORD = os.environ.get("PASSWORD")
GYM_URL = "https://appbrewery.github.io/gym/"


class SeleniunConfigure:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        self.chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(GYM_URL)
        self.CNT_BOOKED_JOINED = 0
        self.CNT_WAITLISTS_JOINED = 0
        self.CNT_ALREADY_BOOKED_OR_WAITLISTED = 0
        self.summary = []

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
            if "Tue" in  day_title or "Thu" in day_title:
                time_tue = card.find_elements(By.CSS_SELECTOR, value = "p[id^='class-time-']")
                class_name = card.find_element(By.CSS_SELECTOR, value="h3[id^=class-name-]").text
                buttons = card.find_elements(By.CSS_SELECTOR, value="button[id^='book-button-']")
                for i, t in enumerate(time_tue):
                    if "6:00 PM" in t.text:
                        click_button = buttons[i]
                        if click_button.text == "Booked":
                            self.CNT_ALREADY_BOOKED_OR_WAITLISTED += 1
                            print(f'✓ Already booked: {class_name} on {day_title} at hout {t.text}')
                            self.summary.append(f"• [Already Booked] {class_name} on {day_title} ({t.text})")
                        elif click_button.text == "Waitlisted":
                            self.CNT_ALREADY_BOOKED_OR_WAITLISTED += 1
                            print(f'✓ Already on Waitlist: {class_name} on {day_title} at hout {t.text}')
                            self.summary.append(f"• [Already Waitlist] {class_name} on {day_title} ({t.text})")
                        elif click_button.text == "Join Waitlist":
                            self.CNT_WAITLISTS_JOINED += 1
                            click_button.click()
                            print(f'✓ Joined Waitlist for: {class_name} on {day_title} at hout {t.text}')
                            self.summary.append(f"• [New Waitlist] {class_name} on {day_title} ({t.text})")
                        else:
                            self.CNT_BOOKED_JOINED +=1
                            click_button.click()
                            print(f"✓ Booked for {class_name} on {day_title} and at hour {t.text}")
                            self.summary.append(f"• [New Booking] {class_name} on {day_title} ({t.text})")

    def verification_bookings(self):
        wait = WebDriverWait(self.driver, 15)

        # --- BOOKINGS SECTION ---
        wait.until(EC.presence_of_all_elements_located((By.ID, "my-bookings-link")))
        my_bookings = self.driver.find_element(By.ID, "my-bookings-link")
        my_bookings.click()

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id^='booking-card']")))
        booking_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[id^='booking-card']")

        print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")
        found_bookings = 0
        for card in booking_cards:
            names = card.find_elements(By.CSS_SELECTOR, "h3[id^='booking-class-']")
            whens = card.find_elements(By.CSS_SELECTOR, "p")
            for i, name in enumerate(names):
                when_text = whens[i].text.replace("When:", "").strip()
                class_name = name.text
                if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
                    found_bookings += 1
                    print(f"  ✓ Verified: {class_name} ({when_text})")

        # --- WAITLIST SECTION ---
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id^='waitlist-section']")))
        waitlist_sections = self.driver.find_elements(By.CSS_SELECTOR, "div[id^='waitlist-section']")

        for section in waitlist_sections:
            names = section.find_elements(By.CSS_SELECTOR, "h3[id^='waitlist-class-']")
            whens = section.find_elements(By.CSS_SELECTOR, "p")

            for i, name in enumerate(names):
                when_text = whens[i].text.replace("When:", "").strip()
                class_name = name.text
                if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
                    found_bookings += 1
                    print(f"  ✓ Verified (Waitlist): {class_name} ({when_text})")

        print("\n--- VERIFICATION RESULT ---")
        expected = self.CNT_BOOKED_JOINED + self.CNT_WAITLISTS_JOINED + self.CNT_ALREADY_BOOKED_OR_WAITLISTED
        print(f"Expected: {expected} bookings")
        print(f"Found: {found_bookings} bookings")

        if expected == found_bookings:
            print("✅ SUCCESS: All bookings verified!")
        else:
            diff = expected - found_bookings
            print(f"❌ MISMATCH: Missing {diff} bookings")

    def booking_summary(self):
        print("--- BOOKING SUMMARY ---")
        print(f"Classes booked: {self.CNT_BOOKED_JOINED}")
        print(f"Waitlists joined: {self.CNT_WAITLISTS_JOINED}")
        print(f"Already Booked/waitlisted: {self.CNT_ALREADY_BOOKED_OR_WAITLISTED}")
        print(f"Total classes processed: {self.CNT_BOOKED_JOINED + self.CNT_WAITLISTS_JOINED + self.CNT_ALREADY_BOOKED_OR_WAITLISTED}")
        print("\n--- DETAILED CLASS LIST ---")
        for line in self.summary:
            print(" ", line)



