import smtplib
import datetime as dt
import pandas
from random import choice
my_email ="fulger.sorin@yahoo.com"
password=""
data = pandas.read_csv("birthdays.csv", index_col=None)
data_dict = data.to_dict(orient="records")
now = dt.datetime.now()
month = now.month
day = now.day
for row in data_dict:
    if row["day"] == day and row["month"] == month:
        random_file = choice(["./letter_templates/letter_1.txt", "./letter_templates/letter_2.txt", "./letter_templates/letter_3.txt"])
        with open(random_file) as file:
            content = file.readlines()
            new_content= "".join(content)
            send_file=new_content.replace("[name]", row["name"])
        with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:
            connection.starttls()  # securizeaza conexiunea
            connection.login(user=my_email, password=password)
            msg = f"From: {my_email}\nTo: {row["email"]}\nSubject: Happy Birthday {row["name"]}\n\n{send_file}"
            connection.sendmail(
                from_addr=my_email,
                to_addrs=row["email"],
                msg=msg
            )
