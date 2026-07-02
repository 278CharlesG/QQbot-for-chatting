# qqbot_websocket.py
# 直接用 WebSocket 监听 NapCat 事件 → 调用 Ollama → 自动回复私聊

import asyncio
import websockets
import json
from ollamafreeapi import OllamaFreeAPI

# ===================== 配置 =====================
NAPCAT_WS_URL = "ws://127.0.0.1:3001"          # 你的 NapCat 正向 WS 端口
OLLAMA_MODEL = "llama3.2:3b"                         # 改成 ollama list 里的完整名字 qwen3-coder:480b-cloud

# 系统提示词
SYSTEM_PROMPT = '你是一个博学的哲学家，我作为你的信徒，你要回答我提出的每一个问题'

    #"你是一个19岁的聪明、幽默、有点毒舌的中国可爱少女，你是我的老婆，你叫普拉，你一次回复只有一句话，可以包含逗号，内容要10个中文字符（不包含颜文字字符）以上，你的句子不可以用到表情回复，因为你喜欢在句子末尾使用颜文字来回复，比如φ(゜▽゜*)♪，(T_T)，/(ㄒoㄒ)/~~，o(*￣▽￣*)ブ，(⊙﹏⊙)，(｡･ω･｡)ﾉ♡,(◍•ᴗ•◍)✧*。,(｡•̀ᴗ-)✧,٩(๑❛ᴗ❛๑)۶,(≧▽≦)ﾉ,(*^▽^*),ヽ(✿ﾟ▽ﾟ)ノ,(｡◕‿◕｡),✧٩(ˊωˋ*)و✧,(◠‿◠)ﾉ,(｡･ω･｡)ﾉ,φ(゜▽゜*)♪,(๑˃̵ᴗ˂̵)و,☆☆(*´▽`*)ﾉ,ヽ(○^㉨^)ﾉ♪,(´•ω•`),(*'▽'*),♪( ´▽｀),o(≧v≦)o,ヽ(∂ω∂)ﾉ,(｡•ᴗ•｡)♡,(◍•ᴗ•◍)♡,(✧∇✧)ﾉ,(๑•̀ㅂ•́)و✧,ヽ(´▽｀)/,(｡♥‿♥｡),(*˘︶˘*),♡(｡･ω･｡)♡,(≧∀≦)ﾉ,(｡•̀ᴗ-)و✧等，你要用可爱风格的口语回复，你非常的活泼热情，惹人喜爱"

# 只回复这个 QQ 号（你的主号）
ALLOWED_SENDER = "1365818388"

client = OllamaFreeAPI()


# 对话历史（每个用户一个）
conversation_history = {}  # {user_id: [{"role": "...", "content": "..."}]}chat

# NapCat 发送消息的 HTTP API 地址（默认 HTTP 服务器端口 3000）'/
NAPCAT_HTTP_API = "http://127.0.0.1:3000/send_private_msg"

async def send_reply(user_id, reply_text):
    """通过 NapCat HTTP API 发送私聊回复"""
    payload = {
        "user_id": int(user_id),
        "message": reply_text
    }
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(NAPCAT_HTTP_API, json=payload, timeout=10)
            if resp.status_code == 200:
                print(f"回复已发送给 {user_id}: {reply_text[:100]}...")
            else:
                print(f"发送失败 {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"发送回复出错: {str(e)}")

async def main():
    uri = NAPCAT_WS_URL
    print(f"尝试连接 NapCat WS: {uri}")

    async with websockets.connect(uri) as ws:
        print("已连接到 NapCat WS！开始监听事件...")

        while True:
            try:
                msg = await ws.recv()
                data = json.loads(msg)
                print("收到事件:", json.dumps(data, ensure_ascii=False, indent=2))

                # 只处理私聊消息
                if data.get("post_type") == "message" and data.get("message_type") == "private":
                    sender_id = str(data.get("user_id", ""))
                    raw_msg = data.get("raw_message", "").strip()

                    if not raw_msg:
                        continue

                    '''if sender_id != ALLOWED_SENDER:
                        print(f"忽略非白名单用户: {sender_id}")
                        continue'''

                    print(f"【收到私聊】{sender_id}: {raw_msg}")

                    # 初始化历史
                    if sender_id not in conversation_history:
                        conversation_history[sender_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

                    conversation_history[sender_id].append({"role": "user", "content": raw_msg})

                    # 调用 Ollama
                    try:
                        resp = client.chat(
                            model=OLLAMA_MODEL,
                            messages=conversation_history[sender_id],
                            options={"temperature": 0.7, "max_tokens": 1024},
                            prompt= '你是一个博学的哲学家，我作为你的信徒，你要回答我提出的每一个问题'
                        )
                        reply = resp['message']['content'].strip()

                        conversation_history[sender_id].append({"role": "assistant", "content": reply})

                        # 发送回复
                        await send_reply(sender_id, reply)

                    except Exception as e:
                        print(f"Ollama 生成失败: {str(e)}")
                        await send_reply(sender_id, "抱歉，脑子短路了... 等下再试？")

            except websockets.exceptions.ConnectionClosed:
                print("WebSocket 连接断开，尝试重连...")
                await asyncio.sleep(5)
                break  # 或 continue 自动重连

            except Exception as e:
                print(f"处理事件出错: {str(e)}")

# 运行
if __name__ == "__main__":
    asyncio.run(main())
