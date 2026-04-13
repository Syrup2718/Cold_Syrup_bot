from database.db import get_connection
import datetime

def insert_msg(message_id, guild_id, channel_id, author_id, author_name, content, created_at):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR IGNORE INTO messages (
            message_id,
            guild_id,
            channel_id,
            author_id,
            author_name,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        message_id,
        guild_id,
        channel_id,
        author_id,
        author_name,
        content,
        created_at
    ))

    conn.commit()
    conn.close()


def get_recent_messages(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            message_id,
            guild_id,
            channel_id,
            author_id,
            author_name,
            content,
            created_at
        FROM messages
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_top_words(guild_id, scope="day", limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT word, count FROM word_frequency
        WHERE scope = ? AND guild_id = ?
        ORDER BY count DESC
        LIMIT ?
    """, (scope, guild_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_member_activity(guild_id, days=1, top=5):
    conn = get_connection()
    cursor = conn.cursor()

    end_time = datetime.datetime.now().isoformat()
    start_time = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()

    cursor.execute("""
        SELECT author_id, author_name, COUNT(*) as message_count
        FROM messages
        WHERE guild_id = ?
          AND created_at BETWEEN ? AND ?
        GROUP BY author_id, author_name
        ORDER BY message_count DESC
        LIMIT ?
    """, (guild_id, start_time, end_time, top))

    rows = cursor.fetchall()
    conn.close()
    return 