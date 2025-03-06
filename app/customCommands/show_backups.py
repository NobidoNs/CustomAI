import os
from datetime import datetime
from app.utils.wright import wright

def show_backups():
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        wright("No backups found. The backups directory does not exist.")
        
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith("output_backup_"):
            timestamp = file[13:-3]  # Extract timestamp from filename
            try:
                date = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
                formatted_date = date.strftime("%d %B %Y, %H:%M:%S")
                backups.append(f"- {formatted_date} ({file})")
            except ValueError:
                backups.append(f"- {file}")
    
    if not backups:
        wright("No backups found in the backups directory.")
        
    wright("Available backups:\n" + "\n".join(sorted(backups, reverse=True)))
