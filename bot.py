import smtplib
import os
from email.message import EmailMessage
import requests
from datetime import date
def get_weather(city="Thiruvananthapuram"):
    url=f"http://wttr.in/{city}?format=3"
    try:        
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"
def get_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        quote = data[0]['q']
        author = data[0]['a']
        return f'"{quote}" - {author}'
        
    except Exception as e:
        return f"Quote unavailable ({e})"
def get_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["text"]

    except Exception as e:
        return f"Fact unavailable ({e})"
def build_summary():
        fact = get_fact()
        today = date.today().strftime("%B %d, %Y")
        weather = get_weather()

        
        quote = get_quote()
        summary = f"""
        ---------------------------
        ---------------------------
        PULSE - Daily Summary
        {today}
        ---------------------------
        ---------------------------
        WEATHER
         {weather}
        RANDOM FACT
         {fact}
        TODAY'S QUOTE
         {quote}
        ---------------------------
        ---------------------------
        """
        return summary
def run():
    summary = build_summary()

    print(summary)

    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    send_email(summary)

    print("pulse ran successfully")
def send_email(summary):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "Pulse Daily Summary"
    msg["From"] = sender
    msg["To"] = sender

    msg.set_content(summary)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        print("Email:", sender)
        print("Password length:", len(password))
        smtp.login(sender, password)
        smtp.send_message(msg)
if __name__ == "__main__":  
    run()
