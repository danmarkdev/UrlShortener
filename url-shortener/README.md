# Shortly - a simple URL shortener

A small Flask web app that turns long URLs into short, shareable links.

## Features
- Paste a long URL, get a short one back
- Visiting the short link redirects to the original URL
- Tracks how many times each short link has been visited

## Tech stack
- Python (Flask)
- Flask-SQLAlchemy (SQLite database)
- HTML/CSS (no frontend framework needed)

## Setup

1. Clone this repository
   ```
   git clone https://github.com/YOUR-USERNAME/url-shortener.git
   cd url-shortener
   ```

2. Create a virtual environment (recommended)
   ```
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the app
   ```
   python app.py
   ```

5. Open your browser to `http://127.0.0.1:5000`

## How it works
- `POST /shorten` takes a long URL from the form, generates a random 6-character code, and saves the pair to the database
- `GET /<short_code>` looks up the code in the database and redirects the visitor to the original URL, incrementing the click count

## Possible next steps
- Add user accounts so people can see all their own links
- Show a simple analytics page (clicks over time)
- Let users pick a custom short code instead of a random one
- Add link expiry dates
