import re
import jieba

# 文字清理函式

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


# 抓取 Discord 自訂 emoji
custom_emoji_pattern = re.compile(r"<:.*?:([0-9]+)>")

# 抓取 Unicode emoji
unicode_emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE)

def extract_emojis(text):
    emojis = []

    # 抓自訂 emoji
    for match in custom_emoji_pattern.findall(text):
        emojis.append(f"<:{match}>")  # 或直接存 ID

    # 抓 Unicode emoji
    emojis.extend(unicode_emoji_pattern.findall(text))

    return emojis
