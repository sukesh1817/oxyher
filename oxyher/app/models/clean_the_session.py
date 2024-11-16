import os
import time

def cleanup_sessions(directory, max_age_days=1):
    now = time.time()
    max_age_seconds = 60

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Get the file's last modified time
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                print(f'Removed old session file: {file_path}')
                
cleanup_sessions('/var/www/oxyher/flask_session/', max_age_days=1)  # Adjust the path and age
