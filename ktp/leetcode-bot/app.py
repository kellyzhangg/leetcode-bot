from flask import Flask, request, jsonify
from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if 'event' in data:
        event = data['event']
        if event.get('type') == 'message' and 'subtype' not in event:
            handle_message(event)
    return jsonify({'status': 'ok'}), 200

def handle_message(event):
    user_id = event.get('user')
    text = event.get('text')

    if text and user_id:
        update_user_input(user_id)

def update_user_input(user_id):
    from datetime import datetime
    import sqlite3

    conn = sqlite3.connect('database/bot_db.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT OR REPLACE INTO users (id, name, last_input)
    VALUES (?, ?, ?)
    ''', (user_id, "User", datetime.now().date()))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(port=3000)
