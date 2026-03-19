from flask import Flask, render_template, request
import os
import threading
import time

app = Flask(__name__)

# Upload folder fix
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')


# ---------------- APR ----------------
@app.route('/apr', methods=['GET', 'POST'])
def apr():
    if request.method == 'POST':
        apr_file = request.files['apr_file']
        cdr_file = request.files['cdr_file']

        # Ensure folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        apr_path = os.path.join(UPLOAD_FOLDER, apr_file.filename)
        cdr_path = os.path.join(UPLOAD_FOLDER, cdr_file.filename)

        apr_file.save(apr_path)
        cdr_file.save(cdr_path)

        from apr_module.main import process_apr
        result = process_apr(apr_path, cdr_path)

        return render_template('result.html', data=result)

    return render_template('apr_upload.html')


# ---------------- FIRST LOGIN ----------------
@app.route('/first-login', methods=['GET', 'POST'])
def first_login():
    if request.method == 'POST':
        file = request.files['file']

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        from first_login_module.main import process_login
        result = process_login(path)

        return render_template('result.html', data=result)

    return render_template('first_login.html')


# ---------------- AUTO RESTART ----------------
def restart_server():
    while True:
        time.sleep(420)  # 7 minutes
        print("Restarting server...")
        os._exit(0)


threading.Thread(target=restart_server, daemon=True).start()


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
