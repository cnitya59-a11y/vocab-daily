import csv
import os
import smtplib
import sys
from datetime import date, datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---- Config ----
SENDER = "cnitya59@gmail.com"
RECEIVER = os.environ.get("RECEIVER_EMAIL") or "cnitya59@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
START_DATE = date(2026, 11, 5)          # Day 1
SITE_URL = os.environ.get("SITE_URL", "")  # optional link to your GitHub Pages site

IST = timezone(timedelta(hours=5, minutes=30))


def load_words():
    with open(os.path.join(os.path.dirname(__file__), "words.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    days = {}
    for r in rows:
        days.setdefault(int(r["day"]), []).append(r)
    return days


def day_number(today, total_days):
    n = (today - START_DATE).days
    # Loops back to Day 1 after the last day, so it never silently stops.
    return (n % total_days) + 1 if n >= 0 else None


def word_block(w):
    return f"""
    <div style="border-left:4px solid #6c4bd8;padding:12px 16px;margin:16px 0;background:#f7f5ff;border-radius:6px">
      <div style="font-size:24px;font-weight:700;color:#2b1d6b">{w['word']}
        <span style="font-size:14px;font-weight:400;color:#777;font-style:italic">&nbsp;{w['part_of_speech']}</span></div>
      <div style="font-size:16px;margin:6px 0;color:#222">{w['meaning']}</div>
      <div style="font-size:15px;color:#555">“{w['example']}”</div>
    </div>"""


def build_email(day, today_words, review_words):
    names = " & ".join(w["word"] for w in today_words)
    subject = f"📚 Words of the day #{day}: {names}"
    review = ""
    if review_words:
        items = "".join(f"<li><b>{w['word']}</b> — {w['meaning']}</li>" for w in review_words)
        review = f"""<div style="margin-top:24px;font-size:14px;color:#555">
          <b>Quick recall (from last week):</b><ul style="margin:6px 0">{items}</ul></div>"""
    link = f'<p style="font-size:13px"><a href="{SITE_URL}">See all past words →</a></p>' if SITE_URL else ""
    html = f"""<div style="font-family:Georgia,serif;max-width:560px;margin:auto;color:#222">
      <p style="font-size:15px;color:#666">Good morning, J ☀️ Day {day}</p>
      {''.join(word_block(w) for w in today_words)}
      <p style="font-size:14px;color:#666">Challenge: use one of these in a message today.</p>
      {review}{link}
    </div>"""
    text = f"Day {day}\n\n" + "\n\n".join(
        f"{w['word']} ({w['part_of_speech']}): {w['meaning']}\n“{w['example']}”" for w in today_words)
    return subject, text, html


def main():
    dry_run = "--dry-run" in sys.argv
    days = load_words()
    today = datetime.now(IST).date()
    if len(sys.argv) > 2 and sys.argv[1] == "--date":
        today = date.fromisoformat(sys.argv[2])
    day = day_number(today, len(days))
    if day is None:
        print(f"Before start date {START_DATE}. Skipping.")
        return
    review_day = day - 7
    subject, text, html = build_email(day, days[day], days.get(review_day, []))

    if dry_run:
        print(subject)
        with open("preview.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Wrote preview.html")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"], msg["From"], msg["To"] = subject, SENDER, RECEIVER
    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(SENDER, APP_PASSWORD.replace(" ", ""))
        s.send_message(msg)
    print(f"Sent Day {day}: {subject}")


if __name__ == "__main__":
    main()
