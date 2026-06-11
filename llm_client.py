import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
MODEL = os.getenv("ANTHROPIC_MODEL", "deepseek-chat")

client = Anthropic(api_key=API_KEY, base_url=BASE_URL)


def call_llm(messages, system=None, tools=None, stream=False, temperature=0.2):
    if not API_KEY:
        raise RuntimeError("未检测到 ANTHROPIC_API_KEY，请先配置环境变量。")

    kwargs = dict(
        model=MODEL,
        messages=messages,
        max_tokens=4096,
        temperature=temperature,
        stream=stream,
    )
    if system:
        kwargs["system"] = system
    if tools:
        kwargs["tools"] = tools

    return client.messages.create(**kwargs)
