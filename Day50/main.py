from tiktok_selenium import SeleniumTikTok

new_web = SeleniumTikTok()
new_web.close_toast()
new_web.login()
new_web.go_to_home()
for i in range (0,10):
    new_web.scroll()