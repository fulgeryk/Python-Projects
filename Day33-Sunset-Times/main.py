import requests
from datetime import datetime
import smtplib
import time

def check_iss_is_close():
    if (MY_LAT -5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG -5 <= iss_longitude <= MY_LONG +5):
        return True
    else:
        return False

def check_if_is_dark():
    if time_now.hour > sunset or time_now.hour < sunrise:
        return True
    else:
        return False

MY_LAT = 47.158455
MY_LONG = 27.601442


my_email = "fulger.sorin@yahoo.com"
password = ""


#Your position is within +5 or -5 degrees of the ISS position.
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

while True:
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])

    response_sunset = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_sunset.raise_for_status()
    data_sunset = response_sunset.json()

    sunrise = int(data_sunset["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sunset["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if check_iss_is_close():
        if check_if_is_dark():
            with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                msg = f"From: {my_email}\nTo: {my_email}\nSubject: ISS is close to you\n\n LOOK UP !!!"
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=my_email,
                    msg=msg
                )
    time.sleep(60)




