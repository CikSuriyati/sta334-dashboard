import os
from flask import Flask, render_template, request, session, redirect, url_for
import gspread
import csv

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")  # change for production

# Try to connect to Google Sheets; if not available, fall back to sample_data.csv
def load_records():
    try:
        gc = gspread.service_account(filename="credentials.json")  # needs credentials.json (step 2)
        sheet = gc.open("STA334_Assessments").sheet1
        return sheet.get_all_records()
    except Exception as e:
        print("Google Sheets not available, loading sample_data.csv. Error:", e)
        recs = []
        if os.path.exists("sample_data.csv"):
            with open("sample_data.csv", newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    recs.append(r)
        return recs

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        records = load_records()
        student = next((r for r in records if r.get("Email","").strip().lower() == email), None)
        if student:
            session["student"] = student
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Email not found. Try again.")
    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    if "student" not in session:
        return redirect(url_for("login"))
    student = session["student"]
    return render_template("dashboard.html", student=student)

@app.route("/logout")
def logout():
    session.pop("student", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    # for local testing only
    app.run(host="127.0.0.1", port=5000, debug=True)
