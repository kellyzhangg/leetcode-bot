import sqlite3
from datetime import datetime, timedelta
from slack_sdk.errors import SlackApiError

def deduct_points():
    conn = sqlite3.connect('database/bot_db.sqlite')
    cursor = conn.cursor()

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    cursor.execute('''
    UPDATE users
    SET points = points - 10
    WHERE last_input < ?
    ''', (yesterday,))

    conn.commit()

    cursor.execute('''
    SELECT id, points FROM users
    WHERE last_input < ?
    ''', (yesterday,))

    for user_id, points in cursor.fetchall():
        send_message(user_id, points)

    conn.close()

def send_message(user_id, points):
    from slack_sdk import WebClient
    from dotenv import load_dotenv

    load_dotenv()
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

    try:
        client.chat_postMessage(
            channel=user_id,
            text=f"Hey <@{user_id}>, you missed your input yesterday! You now have {points} points left."
        )
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == "__main__":
    deduct_points()
