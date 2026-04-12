from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "bot.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    message_id   TEXT PRIMARY KEY,
                    guild_id     TEXT NOT NULL,
                    channel_id   TEXT NOT NULL,
                    author_id    TEXT NOT NULL,
                    author_name  TEXT NOT NULL,
                    content      TEXT NOT NULL,
                    created_at   TEXT NOT NULL
                )''')       

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_created_at
        ON messages(created_at)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_channel_id
        ON messages(channel_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_author_id
        ON messages(author_id)
    """)
    
    conn.commit()

    conn.close()


