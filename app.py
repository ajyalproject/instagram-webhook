from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Ambil Verify Token dari environment variable
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verifikasi Webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Forbidden', 403

    elif request.method == 'POST':
        # Proses event yang dikirim oleh Facebook
        data = request.get_json()
        print("Received Webhook Event:", data)

        # Tambahkan logika pemrosesan di sini jika diperlukan
        return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
