import sqlite3

DATABASE_NAME = "backend/chat.db"

def create_database():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS chats(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_message TEXT,

            ai_reply TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    conn.close()


def save_chat(user_message, ai_reply):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO chats(user_message, ai_reply)

        VALUES (?,?)

    """,(user_message, ai_reply))

    conn.commit()

    conn.close()


def get_chat_history():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT user_message, ai_reply, timestamp

        FROM chats

        ORDER BY id

    """)

    history = cursor.fetchall()

    conn.close()

    return history