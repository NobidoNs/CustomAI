import os
from datetime import datetime
from app.utils.wright import wright

def show_branches():
    branches_dir = "promts"
    if not os.path.exists(branches_dir):
        wright("No branches found. The branches directory does not exist.")
        return

    branches = os.listdir(branches_dir)
    if not branches:
        wright("No branches available.")
        return

    wright("Available branches:\n" + "\n".join(sorted(branches))) 
