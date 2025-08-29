from flask import Flask, render_template
import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 🔑 Replace with your actual Google Sheet ID from the URL
# Example: https://docs.google.com/spreadsheets/d/1XyzAbCdEfGh1234567890/edit#gid=0
SHEET_ID = "1sOX8aqzMiXYnhDz_ihCw5LhDR3atAUlKNHaTcxTVUH0"

def get_sheet_data():
    try:
        # Load Google credentials from environment variable
        google_creds_json = os.getenv("GOOGLE_CREDENTIALS")
        if not google_creds_json:
            raise Exception("GOOGLE_CREDENTIALS not found in environment variables.")

        creds_dict = json.loads(google_creds_json)

        # Define scope
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

        # Connect to Google Sheets using Sheet ID
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1  

        # Convert to DataFrame
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df

    except Exception as e:
        # Fallback to local CSV if Sheets fails
        print(f"Google Sheets not available, loading sample_data.csv. Error: {e}")
        return pd.read_csv("sample_data.csv")

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
