# vocab-daily

2 new vocab words emailed every morning at 8:15 AM IST, plus a website with today's words and the full archive.

- `words.csv` — 730 words (2/day × 365 days). Edit freely; keep the `day` column.
- `send_vocab.py` — sends the email via Gmail SMTP. Day 1 = 5 Nov 2026. Loops back to Day 1 after Day 365.
- `.github/workflows/vocab_daily.yml` — daily schedule + manual "Run workflow" button.
- `index.html` — the website (GitHub Pages).

Each email also includes a quick recall of the words from 7 days earlier.

## Secrets (Settings → Secrets and variables → Actions)
- `GMAIL_APP_PASSWORD` — same app password as goodmorning-rumm (no spaces)
- `RECEIVER_EMAIL` — where the words go (defaults to cnitya59@gmail.com)

Optional variable (Variables tab): `SITE_URL` — your GitHub Pages link, adds an archive link to each email.

## Test locally
`python send_vocab.py --date 2026-11-05 --dry-run` → writes `preview.html`
