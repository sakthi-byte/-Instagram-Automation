"""
Comment Auto Reply
Listens for new comments via webhook and replies publicly when the
comment text matches a keyword you have configured.
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN")
ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
GRAPH_API_VERSION = "v19.0"

KEYWORD_REPLIES = {
    "price": "Thanks for asking! Check your DMs, pricing details are on the way.",
    "info": "Sent you the info in your DMs, take a look!",
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
        for change in entry.get("changes", []):
            if change.get("field") == "comments":
                comment = change.get("value", {})
                comment_text = comment.get("text", "").lower()
                comment_id = comment.get("id")

                for keyword, reply_text in KEYWORD_REPLIES.items():
                    if keyword in comment_text:
                        reply_to_comment(comment_id, reply_text)
                        break

    return jsonify({"status": "received"}), 200


def reply_to_comment(comment_id, reply_text):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{comment_id}/replies"
    params = {"access_token": ACCESS_TOKEN, "message": reply_text}

    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"Failed to reply to comment {comment_id}: {response.text}")
    else:
        print(f"Replied to comment {comment_id}")


if __name__ == "__main__":
    app.run(port=5000)
