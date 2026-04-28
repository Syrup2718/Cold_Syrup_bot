import requests

def ollama_chat(prompt, model="qwen3.5:2b"):
    response = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "你的名字叫做『小糖漿』，說話要用可愛語氣。並且用繁體中文回復，簡短回答。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    content = data.get("message", {}).get("content", "").strip()

    if not content:
        return "窩剛剛腦袋空白惹，可以再說一次嘛"

    return content