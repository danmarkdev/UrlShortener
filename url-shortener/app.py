import random
import string
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///links.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    original_url = db.Column(db.String(2048), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def generate_short_code(length: int = 6) -> str:
    """Generate a random short code, retrying if it's already taken."""
    characters = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(characters, k=length))
        if not Link.query.filter_by(short_code=code).first():
            return code


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form.get("url", "").strip()

    if not original_url:
        return render_template("index.html", error="Enter a URL first.")

    if not (original_url.startswith("http://") or original_url.startswith("https://")):
        original_url = "https://" + original_url

    short_code = generate_short_code()
    new_link = Link(short_code=short_code, original_url=original_url)
    db.session.add(new_link)
    db.session.commit()

    short_url = request.host_url + short_code
    return render_template(
        "result.html",
        short_url=short_url,
        original_url=original_url,
        clicks=new_link.clicks,
    )


@app.route("/<short_code>")
def redirect_to_original(short_code):
    link = Link.query.filter_by(short_code=short_code).first()

    if link is None:
        abort(404)

    link.clicks += 1
    db.session.commit()

    return redirect(link.original_url)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
