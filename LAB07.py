from aiot_tools import *

# 依序填入你的 PAT、定義助理角色的系統訊息，以及具體的提示詞
GITHUB_TOKEN = "你的 PAT"
SYSTEM = "請以繁體中文回覆"
PROMPT = "你是誰"

# 連線 Wi-Fi
connect_wifi()
# 發送請求到 LLM API
call_llm(SYSTEM, PROMPT, model="openai/gpt-4.1-mini", bearer_token=GITHUB_TOKEN)