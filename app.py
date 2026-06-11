import gradio as gr
from agent import run_agent_stream
from tools import generate_pdf as gen_pdf_tool


EXAMPLE_INPUT = """我写了一个查找数组中两个数之和等于 target 的算法，现在使用双重循环，时间复杂度是 O(n²)。请帮我优化这个算法，并说明优化前后的复杂度变化。

原始代码：

def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
"""

# Holds the latest agent result so the PDF button can access it
_latest_result = ""


def fill_example():
    return EXAMPLE_INPUT


def optimize(user_input):
    global _latest_result
    if not user_input or not user_input.strip():
        yield ("❌ **错误：请输入需要优化的内容**", "", gr.update(interactive=False), None)
        return

    for status, result, pdf in run_agent_stream(user_input):
        _latest_result = result
        yield (status, result, gr.update(interactive=False), None)

    yield ("🎉 **优化完成！**", _latest_result, gr.update(interactive=True), None)


def generate_pdf_with_progress(progress=gr.Progress()):
    global _latest_result
    if not _latest_result:
        return None

    progress(0.1, desc="📄 正在准备报告内容...")
    import time
    time.sleep(0.2)

    progress(0.4, desc="🔨 正在生成 PDF 文件...")
    result = gen_pdf_tool(content=_latest_result)
    pdf_path = result.get("path")

    progress(0.8, desc="💾 正在保存文件...")
    time.sleep(0.2)

    progress(1.0, desc="✅ PDF 已生成")
    return pdf_path


with gr.Blocks(title="智解 Agent") as demo:
    gr.Markdown(
        """
        # 智解 Agent：通用问题优化与求解智能体

        输入你希望优化的问题、算法、代码或方案，系统将自动分析瓶颈、生成优化策略、输出优化后方案。
        """
    )

    with gr.Row(equal_height=False):
        with gr.Column(scale=2, min_width=400):
            user_input = gr.Textbox(
                label="📝 输入",
                lines=18,
                placeholder="可以输入算法、代码、学习计划、项目方案等。",
            )

            with gr.Row():
                example_btn = gr.Button("📋 一键填充 Two Sum 示例", size="sm")
                run_btn = gr.Button("🚀 开始优化", variant="primary", size="lg")

        with gr.Column(scale=3, min_width=500):
            status_md = gr.Markdown(
                "👆 在左侧输入内容后点击「开始优化」", container=True
            )

            result_output = gr.Markdown(label="📄 优化结果", container=True)

            with gr.Row():
                pdf_btn = gr.Button(
                    "📥 生成 PDF 报告", variant="secondary", interactive=False
                )

            pdf_output = gr.File(label="📥 下载 PDF 报告")

    example_btn.click(fn=fill_example, inputs=[], outputs=[user_input])

    run_btn.click(
        fn=optimize,
        inputs=[user_input],
        outputs=[status_md, result_output, pdf_btn, pdf_output],
    )

    pdf_btn.click(
        fn=generate_pdf_with_progress,
        inputs=[],
        outputs=[pdf_output],
    )


if __name__ == "__main__":
    demo.queue()
    demo.launch()
