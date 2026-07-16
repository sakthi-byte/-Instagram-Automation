"""
DM Auto Reply
Listens for incoming direct messages via webhook and replies
automatically when the message text matches a configured keyword.
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN")
ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
GRAPH_API_VERSION = "v19.0"

KEYWORD_REPLIES = {
    "price": "Here is our current pricing: https://example.com/pricing",
    "hours": "We are open Monday to Saturday, 9am to 6pm.",
}


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.get_json()

    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            sender_id = messaging_event.get("sender", {}).get("id")
            message_text = messaging_event.get("message", {}).get("text", "").lower()

            if not sender_id or not message_text:
                continue

            for keyword, reply_text in KEYWORD_REPLIES.items():
                if keyword in message_text:
                    send_dm(sender_id, reply_text)
                    break

    return jsonify({"status": "received"}), 200


def send_dm(recipient_id, message_text):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
    }
    params = {"access_token": ACCESS_TOKEN}

    response = requests.post(url, json=payload, params=params)

    if response.status_code != 200:
        print(f"Failed to send DM to {recipient_id}: {response.text}")
    else:
        print(f"DM sent to {recipient_id}")


if __name__ == "__main__":
    app.run(port=5001)
