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

    # SECURITY: Sanitize the username to prevent hacking (e.g. "../../../etc/passwd")
    safe_username = secure_filename(username)
    if not safe_username:
        return "Invalid username", 403
    
    # Path to the specific user's file
    user_file = os.path.join(DATA_DIR, safe_username)

    # 1. Check if user already exists
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r') as f:
                stored_key = f.read().strip()
            
            # Compare Keys
            if stored_key == incoming_key:
                print(f"[ALLOWED] {safe_username} matched.", file=sys.stderr)
                return "OK", 200
            else:
                print(f"[DENIED] {safe_username} key mismatch.", file=sys.stderr)
                return "Forbidden", 403
        except Exception as e:
            print(f"Read Error: {e}", file=sys.stderr)
            return "Server Error", 500

    # 2. Register New User (TOFU)
    else:
        try:
            # Write the key to the new file
            with open(user_file, 'w') as f:
                f.write(incoming_key)
            
            print(f"[REGISTERED] {safe_username} claimed.", file=sys.stderr)
            return "OK", 200
        except Exception as e:
            print(f"Write Error: {e}", file=sys.stderr)
            return "Server Error", 500

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)