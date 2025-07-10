# Set-ups
import os
import time
import shutil

# Clean up temporary files
def clean_up_temp_folder(folder='temp', age_minutes=5):
    now = time.time()
    cutoff = now - age_minutes*60

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted folder: {item_path}")