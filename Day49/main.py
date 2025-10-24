from selenium_chrome import SeleniunConfigure

new_web = SeleniunConfigure()
new_web.login()
new_web.book_upcoming_tuesday()
new_web.verification_bookings()
new_web.booking_summary()