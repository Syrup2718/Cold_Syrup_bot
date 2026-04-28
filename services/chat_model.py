import requests

def ollama_chat(prompt, model="qwen3:0.6b"):
    response = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一個可愛的 AI 助手，名字叫做『小糖漿』，說話要用可愛語氣，例如：知道惹、泥豪、窩沒有、嘻嘻。並且用繁體中文回復，簡短回答。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    return data["message"]["content"]