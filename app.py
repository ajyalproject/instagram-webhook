from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)

# Endpoint untuk verifikasi Webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verifikasi Webhook dengan token
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Forbidden', 403

    elif request.method == 'POST':
        # Proses pesan yang masuk
        data = request.json
        if data.get('entry'):
            for entry in data['entry']:
                messaging = entry.get('messaging', [])
                for message_event in messaging:
                    sender_id = message_event['sender']['id']
                    if 'message' in message_event:  # Pesan diterima
                        user_message = message_event['message'].get('text', '')
                        response_message = generate_response(user_message)
                        send_message(sender_id, response_message)
        return 'EVENT_RECEIVED', 200


# Fungsi untuk mengirim pesan menggunakan Graph API
def send_message(recipient_id, message):
    url = f"https://graph.facebook.com/v16.0/me/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")


# Fungsi untuk membuat respons (sederhana)
def generate_response(user_message):
    if "halo" in user_message.lower():
        return "Halo! Ada yang bisa saya bantu?"
    elif "bye" in user_message.lower():
        return "Sampai jumpa! Semoga harimu menyenangkan!"
    else:
        return "Maaf, saya belum mengerti pesan Anda. Bisa dijelaskan lebih detail?"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
