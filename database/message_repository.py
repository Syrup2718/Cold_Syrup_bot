from database.db import get_connection
from services.text_cleaner import extract_emojis
import datetime

# 負責從DB抓取資料

def to_utc_iso(dt: datetime.datetime) -> str:
    # 確保時間統一為 UTC ISO 格式
    if dt.tzinfo is None:
        dt = dt.astimezone(datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)
    return dt.isoformat()


# 新增記錄
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

# 
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

# 群組成員活躍度DB抓取
def get_member_activity(guild_id, days=1, top=5):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = to_utc_iso(now)
    start_time = to_utc_iso(now - datetime.timedelta(days=days))

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
    return rows

# 個人活躍度DB抓取
def get_user_activity(guild_id, user_id, days=1):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = now.isoformat()
    start_time = (now - datetime.timedelta(days=days)).isoformat()

    # 個人訊息數
    cursor.execute("""
        SELECT COUNT(*) 
        FROM messages
        WHERE guild_id = ?
          AND author_id = ?
          AND created_at BETWEEN ? AND ?
    """, (guild_id, str(user_id), start_time, end_time))
    user_count = cursor.fetchone()[0]

    # 群組總訊息數
    cursor.execute("""
        SELECT COUNT(*)
        FROM messages
        WHERE guild_id = ?
          AND created_at BETWEEN ? AND ?
    """, (guild_id, start_time, end_time))
    total_count = cursor.fetchone()[0]

    conn.close()
    return user_count, total_count


def get_top_emojis(guild_id, days=3, top=5):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = (now - datetime.timedelta(days=days)).isoformat()

    cursor.execute("""
        SELECT content
        FROM messages
        WHERE guild_id = ?
        AND created_at >= ?
    """, (guild_id, start_time))

    rows = cursor.fetchall()
    conn.close()

    emoji_counts = {}
    for row in rows:
        emojis = extract_emojis(row[0])
        for e in emojis:
            emoji_counts[e] = emoji_counts.get(e, 0) + 1

    sorted_emojis = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_emojis[:top]
