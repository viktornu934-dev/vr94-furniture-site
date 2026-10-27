from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-publishing"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LEADS_FILE = DATA_DIR / "requests.csv"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/request", methods=["POST"])
def submit_request():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    service = request.form.get("service", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not phone:
        flash("Пожалуйста, укажите имя и номер телефона.")
        return redirect(url_for("index") + "#contacts")

    new_file = not LEADS_FILE.exists()
    with LEADS_FILE.open("a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["Дата", "Имя", "Телефон", "Услуга", "Комментарий"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name, phone, service, message
        ])

    flash("Спасибо! Заявка сохранена. Мы свяжемся с вами.")
    return redirect(url_for("index") + "#contacts")

if __name__ == "__main__":
    app.run(debug=True)
