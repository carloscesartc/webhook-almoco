from flask import Flask, request, jsonify
from datetime import datetime, time
import requests
import os

app = Flask(__name__)

CHATWOOT_API_URL = os.getenv("CHATWOOT_API_URL")
CHATWOOT_API_TOKEN = os.getenv("CHATWOOT_API_TOKEN")

@app.route("/webhook-almoco", methods=["POST"])
def webhook():
    payload = request.json
    now = datetime.now().time()
    if time(12, 0) <= now <= time(13, 30):
        conversation = payload.get("conversation")
        if conversation:
            conversation_id = conversation.get("id")
            account_id = payload.get("account", {}).get("id")
            send_auto_reply(account_id, conversation_id)
    return jsonify({"status": "ok"}), 200

def send_auto_reply(account_id, conversation_id):
    url = f"{CHATWOOT_API_URL}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
    headers = {
        "api_access_token": CHATWOOT_API_TOKEN
    }
    data = {
        "content": "Olá! Nosso horário de atendimento vai das 08h30 às 12h e das 13h30 às 17h55. Voltamos em breve!",
        "message_type": "outgoing"
    }
    response = requests.post(url, json=data, headers=headers)
    print("Resposta da API Chatwoot:", response.status_code, response.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
