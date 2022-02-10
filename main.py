import datetime as dt
import sys
import random
import smtplib

from dotenv import dotenv_values
import pandas

config = dotenv_values(".env")

data = pandas.read_csv("birthdays.csv")
birthdays = data.to_dict(orient="records")


# 2. Check if today matches a birthday in the birthdays.csv
now = dt.datetime.now()
month = now.month

todays_birthdays = [b for b in birthdays if b["month"] == now.month and b["day"] == now.day]

if len(todays_birthdays) == 0:
    sys.exit()

todays_birthday = todays_birthdays[0]

template = f"letter_{random.randint(1, 3)}.txt"
with open(f"letter_templates/{template}") as file:
    data = file.read()
    letter = data.replace("[NAME]", todays_birthday["name"])

my_email = config["email"]
password = config["password"]
gmail_smtp_address = "smtp.gmail.com"

with smtplib.SMTP(gmail_smtp_address) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=todays_birthday["email"],
        msg=f"Subject:Happy Birthday!\n\n{letter}"
    )



