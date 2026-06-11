import os
import sys
from dotenv import load_dotenv
from llm_client import get_client, get_model
from prompts import OPTIMIZER_SYSTEM_PROMPT

print(f"[DEBUG] agent.py 导入时 os.environ KEYS: {list(os.environ.keys())}", flush=True)
print(f"[DEBUG] agent.py 导入时 ANTHROPIC_API_KEY 存在: {os.getenv('ANTHROPIC_API_KEY') is not None}", flush=True)
sys.stdout.flush()


def run_agent_stream(user_input: str):
    """Generator yielding (status_md, result_md, pdf_path).

    Pure streaming LLM call — no tools. PDF generation is handled
    by the UI button separately.
    """
    if not user_input or not user_input.strip():
        yield ("❌ **输入为空**", "", None)
        return

    load_dotenv()

    # --- 环境变量诊断 ---
    print("=" * 50, flush=True)
    print("[DEBUG] load_dotenv() 完成", flush=True)
    print(f"[DEBUG] os.environ 中所有 KEY: {list(os.environ.keys())}", flush=True)
    print(f"[DEBUG] ANTHROPIC_API_KEY 存在: {os.getenv('ANTHROPIC_API_KEY') is not None}", flush=True)
    print(f"[DEBUG] DEEPSEEK_API_KEY 存在: {os.getenv('DEEPSEEK_API_KEY') is not None}", flush=True)
    print(f"[DEBUG] ANTHROPIC_BASE_URL = {os.getenv('ANTHROPIC_BASE_URL', '未设置')}", flush=True)
    print(f"[DEBUG] ANTHROPIC_MODEL = {os.getenv('ANTHROPIC_MODEL', '未设置')}", flush=True)
    key_vars = {k: v for k, v in os.environ.items() if 'KEY' in k.upper() or 'API' in k.upper() or 'TOKEN' in k.upper() or 'SECRET' in k.upper()}
    print(f"[DEBUG] 敏感相关环境变量: { {k: v[:8] + '...' if v else '<空>' for k, v in key_vars.items()} }", flush=True)
    print("=" * 50, flush=True)
    # -------------------

    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("DEEPSEEK_API_KEY"):
        yield ("❌ **配置错误**", "未检测到 ANTHROPIC_API_KEY。", None)
        return

    messages = [{"role": "user", "content": user_input}]
    full_result = ""

    yield ("🔄 **正在分析...**", "", None)

    client = get_client()
    model = get_model()

    with client.messages.stream(
        model=model,
        system=OPTIMIZER_SYSTEM_PROMPT,
        messages=messages,
        max_tokens=4096,
        temperature=0.2,
    ) as stream:
        for text in stream.text_stream:
            full_result += text
            yield ("🔄 **正在生成...**", full_result, None)

    yield ("🎉 **优化完成！**", full_result, None)
