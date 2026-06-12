import os
import requests
import smtplib

from bs4 import BeautifulSoup
from email.mime.text import MIMEText

sites = [
    "https://news.ycombinator.com/",
    "https://www.bbc.com/news"
]

html = """
<h1>📰 Daily News Digest</h1>
"""

for site in sites:

    try:
        response = requests.get(site, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        html += f"<h2>{site}</h2><ul>"

        headlines = soup.find_all(["h1", "h2", "h3", "a"])

        count = 0

        for item in headlines:

            text = item.get_text(strip=True)

            if len(text) > 20:

                html += f"<li>{text}</li>"

                count += 1

            if count == 5:
                break

        html += "</ul>"

    except Exception as e:
        html += f"<p>Error reading {site}</p>"

sender = os.environ.get("EMAIL_SENDER")
password = os.environ.get("EMAIL_PASSWORD")
receiver = os.environ.get("EMAIL_RECEIVER")

msg = MIMEText(html, "html")

msg["Subject"] = "Daily News Digest"
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.send_message(msg)

print("News digest sent")