import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import feedparser

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

sites = [
    ("Hacker News", "https://news.ycombinator.com/rss"),
    ("BBC News", "https://feeds.bbci.co.uk/news/rss.xml"),
    ("Reuters", "https://feeds.reuters.com/reuters/topNews")
]

html = f"""
<h1>📰 Daily News Digest</h1>
<p>Top headlines collected automatically.</p>
<p>Generated on: {current_time}</p>
"""

for source_name, feed_url in sites:

    html += f"<h2>{source_name}</h2><ul>"

    try:
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            html += "<li>No headlines found.</li>"

        for entry in feed.entries[:5]:

            title = entry.title
            link = entry.link

            html += f"""
            <li>
                <strong>{title}</strong><br>
                <a href="{link}">Read More</a>
            </li>
            """

    except Exception as e:

        html += f"""
        <li>
            Error fetching headlines: {e}
        </li>
        """

    html += "</ul>"

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

print("News digest sent successfully")