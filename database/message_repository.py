from database.db import get_connection

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