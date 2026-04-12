import re
import jieba

def clean_text(content: str) -> str:
    # 移除網址
    content = re.sub(r'http\S+', '', content)
    # 移除 spoiler (||內容||)
    content = re.sub(r'\|\|.*?\|\|', '', content)
    # 移除刪除線 (~~內容~~)
    content = re.sub(r'~~.*?~~', '', content)
    # 移除粗體/斜體 (**內容** 或 *內容*)
    content = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', content)
    # 移除多餘空白
    content = re.sub(r'\s+', ' ', content)
    # 英文字母小寫化
    content = content.lower()
    return content.strip()

def normalize_mentions_and_emojis(content: str) -> str:
    # 將 TAG 轉換成 @user_xxx
    content = re.sub(r'<@!?(\d+)>', r'@user_\1', content)
    # 將伺服器 emoji 轉換成 emoji_name
    content = re.sub(r'<:([a-zA-Z0-9_]+):\d+>', r'\1', content)
    # 保留純 emoji，不移除
    return content

def tokenize(content: str):
    # 先清洗
    cleaned = clean_text(content)
    normalized = normalize_mentions_and_emojis(cleaned)
    # 中文斷詞 + 英文分詞
    return list(jieba.cut(normalized))
