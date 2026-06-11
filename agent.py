import os
from dotenv import load_dotenv
from llm_client import client, MODEL
from prompts import OPTIMIZER_SYSTEM_PROMPT


def run_agent_stream(user_input: str):
    """Generator yielding (status_md, result_md, pdf_path).

    Pure streaming LLM call — no tools. PDF generation is handled
    by the UI button separately.
    """
    if not user_input or not user_input.strip():
        yield ("❌ **输入为空**", "", None)
        return

    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("DEEPSEEK_API_KEY"):
        yield ("❌ **配置错误**", "未检测到 ANTHROPIC_API_KEY。", None)
        return

    messages = [{"role": "user", "content": user_input}]
    full_result = ""

    yield ("🔄 **正在分析...**", "", None)

    with client.messages.stream(
        model=MODEL,
        system=OPTIMIZER_SYSTEM_PROMPT,
        messages=messages,
        max_tokens=4096,
        temperature=0.2,
    ) as stream:
        for text in stream.text_stream:
            full_result += text
            yield ("🔄 **正在生成...**", full_result, None)

    yield ("🎉 **优化完成！**", full_result, None)
