from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import sys

app = Flask(__name__)
DATA_DIR = "/data"

@app.route('/', methods=['POST'])
def auth():
    if not request.is_json:
        return "Invalid JSON", 400
    
    data = request.json
    username = data.get('user')
    incoming_key = data.get('auth_key')

    if not username or not incoming_key:
        return "Missing data", 403

    safe_username = secure_filename(username)
    if not safe_username:
        return "Invalid username", 403
    
    user_file = os.path.join(DATA_DIR, safe_username)

    # --- ATTEMPT 1: Try to Read (Authentication) ---
    # We check if it exists first to allow the user in.
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r') as f:
                stored_key = f.read().strip()
            
            if stored_key == incoming_key:
                print(f"[ALLOWED] {safe_username} matched.", file=sys.stderr)
                return "OK", 200
            else:
                print(f"[DENIED] {safe_username} key mismatch.", file=sys.stderr)
                return "Forbidden", 403
        except Exception as e:
            print(f"Read Error: {e}", file=sys.stderr)
            return "Server Error", 500

    # --- ATTEMPT 2: Try to Write (Registration) ---
    # We use mode='x' (Exclusive Creation). 
    # This FAILS if the file exists, making it impossible to overwrite.
    try:
        with open(user_file, 'x') as f:
            f.write(incoming_key)
        print(f"[REGISTERED] {safe_username} claimed.", file=sys.stderr)
        return "OK", 200
    except FileExistsError:
        # This catches the race condition where someone claimed it
        # immediately after our check above.
        print(f"[RACE CONDITION] {safe_username} was just claimed by someone else.", file=sys.stderr)
        return "Forbidden", 403
    except Exception as e:
        print(f"Write Error: {e}", file=sys.stderr)
        return "Server Error", 500

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)