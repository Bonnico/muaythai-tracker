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



def view_sessions():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet.")
        return
    
    df = pd.read_csv(LOG_FILE)
    print("\n--- Your Training Sessions ---")
    print(df.to_string(index=False))
    print(f"\nTotal sessions: {len(df)}")
    print(f"Total training time: {df['duration_min'].sum()} minutes")
    print(f"Average intensity: {df['intensity'].mean():.1f}/10")

print("\nWhat do you want to do?")
print("1 - Log a session")
print("2 - View all sessions")
choice = input("Enter 1 or 2: ")

if choice == "1":
    log_session()
elif choice == "2":
    view_sessions()
else:
    print("Invalid choice.")