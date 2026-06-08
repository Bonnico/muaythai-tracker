import pandas as pd
import os
from datetime import date

LOG_FILE = "data/sessions.csv"

def log_session():
    print("\n--- Log Training Session ---")
    session_date = str(date.today())
    session_type = input("Session type (bag work / sparring / clinch / conditioning): ")
    duration = int(input("Duration in minutes: "))
    intensity = int(input("Intensity 1-10: "))
    notes = input("Any notes (injuries, focus, felt good/bad): ")

    session = {
        "date": session_date,
        "type": session_type,
        "duration_min": duration,
        "intensity": intensity,
        "notes": notes
    }

    df_new = pd.DataFrame([session])

    if os.path.exists(LOG_FILE):
        df_existing = pd.read_csv(LOG_FILE)
        df = pd.concat([df_existing. df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(LOG_FILE, index=False)
    print(f"\nSession logged. Total sessions: {len(df)}")

log_session()