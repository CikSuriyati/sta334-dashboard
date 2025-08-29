from flask import Flask, render_template
import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

def get_sheet_data():
    # Load Google credentials from environment variable
    google_creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(google_creds_json)

    # Define scope
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

    # Connect to Google Sheets
    client = gspread.authorize(creds)

    # ⚠️ Replace with the exact name of your sheet
    sheet = client.open("STA334 Marks").sheet1  

    # Get all rows as list of dicts → convert to DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

@app.route("/")
def index():
    df = get_sheet_data()
    return render_template(
        "index.html",
        tables=[df.to_html(classes='data table table-bordered table-striped', index=False)],
        titles=df.columns.values
    )

if __name__ == "__main__":
    app.run(debug=True)
