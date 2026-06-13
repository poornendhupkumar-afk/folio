import os
import requests
import smtplib
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

sites = [
    "https://news.ycombinator.com/",
    "https://www.bbc.com/news",
    "https://www.reuters.com/world/"
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

                html += f"""
                <li>
                    {text}<br>
                    Published: {current_time}<br>
                    <a href="{site}">Source</a>
                </li>
                """

                count += 1

            if count == 5:
                break

        html += "</ul>"

    except Exception as e:
        html += f"<p>Error reading {site}: {e}</p>"

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