from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "bot.db"

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
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


def init_word_freq_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_frequency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id TEXT NOT NULL,
            word TEXT NOT NULL,
            count INTEGER NOT NULL,
            date TEXT NOT NULL,
            scope TEXT NOT NULL  -- 'day', 'week', 'month'
        )
    ''')

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_word_frequency_guild
        ON word_frequency(guild_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_word_frequency_word
        ON word_frequency(word)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_word_frequency_date
        ON word_frequency(date)
    """)

    conn.commit()
    conn.close()
