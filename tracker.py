import pandas as pd
import os
from datetime import date
import matplotlib.pyplot as plt

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
        df = pd.concat([df_existing, df_new], ignore_index=True)
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


def filter_sessions():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet.")
        return
    
    df = pd.read_csv(LOG_FILE)
    print("\nSession types in your log:", df['type'].unique())
    session_type = input("Enter session type to filter: ")

    filtered = df[df['type'].str.lower() == session_type.lower()]

    if filtered.empty:
        print(f"No sessions found for type: {session_type}")
        return

    print(f"\n--- {session_type.upper()} Sessions ---")
    print(filtered.to_string(index=False))
    print(f"\nTotal {session_type} sessions: {len(filtered)}")
    print(f"Total time: {filtered['duration_min'].sum()} minutes")
    print(f"Average intensity: {filtered['intensity'].mean():.1f}/10")

def filter_by_date():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet.")
        return
    
    df = pd.read_csv(LOG_FILE)
    df['date'] = pd.to_datetime(df['date'])

    print("\nEnter date range (YYYY-MM-DD format)")
    start = input("Start date: ")
    end = input("End date: ")

    try:
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    
    filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if filtered.empty:
        print("No sessions found in that date range.")
        return
    
    print(f"\n--- Sessions from {start} to {end} ---")
    print(filtered.to_string(index=False))
    print(f"\nTotal sessions: {len(filtered)}")
    print(f"Total training time: {filtered['duration_min'].sum()} minutes")
    print(f"Average intensity: {filtered['intensity'].mean():.1f}/10")
        
def visualize_sessions():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet.")
        return
    
    df = pd.read_csv(LOG_FILE)
    df['date'] = pd.to_datetime(df['date'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(df['date'], df['intensity'], marker='o', color='red', linewidth=2)
    ax1.set_title('Training Intensity Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Intensity (1-10)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)

    type_counts = df['type'].value_counts()
    ax2.bar(type_counts.index, type_counts.values, color='red', alpha=0.7)
    ax2.set_title('Sessions by Type')
    ax2.set_xlabel('Session Type')
    ax2.set_ylabel('Count')

    plt.tight_layout()
    plt.savefig('data/training_overview.png')
    plt.show()
    print("\nChart saved to data/training_overview.png")

def weekly_summary():
    if not os.path.exists(LOG_FILE):
        print("No sessions logged yet.")
        return
    
    df = pd.read_csv(LOG_FILE)
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.isocalendar().year

    summary = df.groupby(['year', 'week']).agg(
        total_session=('type', 'count'),
        total_minutes = ('duration_min', 'sum'),
        avg_intensity=('intensity', 'mean')
    ).reset_index()

    summary['avg_intensity'] = summary['avg_intensity'].round(1)

    print("\n--- Weekly Training Summary ---")
    print(summary.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 5))
    weeks = [f"W{row.week}" for row in summary.itertuples()]
    ax.bar(weeks, summary['total_minutes'], color='red', alpha=0.7)
    ax.set_title('Weekly Training Volume (minutes)')
    ax.set_xlabel('Week')
    ax.set_ylabel('Total Minutes')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('data/weekly_summary.png')
    plt.show()
    print("\nChart saved to data/weekly_summary.png")


print("\nWhat do you want to do?")
print("1 - Log a session")
print("2 - View all sessions")
print("3 - Filter by session type")
print("4 - Filter by date range")
print("5 - Visualize training data")
print("6 - Weekly summary")
choice = input("Enter 1, 2, 3, 4, 5, or 6: ")

if choice == "1":
    log_session()
elif choice == "2":
    view_sessions()
elif choice == "3":
    filter_sessions()
elif choice == "4":
    filter_by_date()
elif choice == "5":
    visualize_sessions()
elif choice == "6":
    weekly_summary()
else:
    print("Invalid choice.")