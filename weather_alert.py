import os
import requests
import smtplib
from email.mime.text import MIMEText

CITY = "Kochi"

API_KEY = os.environ.get("WEATHER_API_KEY")

url = (
    f"https://api.openweathermap.org/data/2.5/weather?"
    f"q={CITY}&appid={API_KEY}&units=metric"
)

data = requests.get(url).json()

temp = data["main"]["temp"]
condition = data["weather"][0]["main"]

if temp > 35 or "rain" in condition.lower():

    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    body = f"""
Weather Alert

City: {CITY}
Temperature: {temp}°C
Condition: {condition}
"""

    msg = MIMEText(body)

    msg["Subject"] = "Weather Alert"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    print("Weather alert sent")

else:
    print("No alert needed")