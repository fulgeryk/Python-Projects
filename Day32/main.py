import smtplib
import datetime as dt
from random import choice
now = dt.datetime.now()
day_of_week = now.weekday()
my_email = "fulger.sorin@yahoo.com"
password=""
if day_of_week == 5:
    with open("quotes.txt") as file:
        data_file = file.readlines()
        quote = choice(data_file)
    with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:
        connection.starttls() #securizeaza conexiunea
        connection.login(user=my_email, password=password)
        msg = f"From: {my_email}\nTo: fulgeryk_cs@yahoo.com\nSubject: Motivation\n\n{quote}"
        connection.sendmail(
            from_addr=my_email,
            to_addrs="fulgeryk_cs@yahoo.com",
            msg=msg
        )




