# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements.txt
python app.py
```

## Environment Variables

- `ANTHROPIC_API_KEY` (required) — DeepSeek API key (also falls back to `DEEPSEEK_API_KEY`)
- `ANTHROPIC_BASE_URL` (optional, default: `https://api.deepseek.com/anthropic`)
- `ANTHROPIC_MODEL` (optional, default: `deepseek-chat`)

## Architecture — Pure Streaming LLM

Gradio web app where users input a problem and get an optimized solution with PDF report. Simple architecture — one streaming LLM call, no agent loop, no tool calls during streaming.

### Flow

```
User Input → Single streaming LLM call → UI updates token-by-token
                                        ↓
                              User clicks "Generate PDF" button → markdown-pdf → download
```

### Files

| File | Role |
|------|------|
| `app.py` | Gradio UI, generator fn for streaming + PDF button with progress bar |
| `agent.py` | Single `client.messages.stream()` call, yields (status, result, pdf_path) |
| `llm_client.py` | Anthropic SDK client pointing at DeepSeek's anthropic-compatible endpoint |
| `tools.py` | `generate_pdf()` using `markdown-pdf` with CJK font CSS |
| `prompts.py` | System prompt with 9-section output structure |
| `setup.sh` | ModelScope system deps (CJK fonts) |

### Key Design Points

- **Pure streaming**: single `client.messages.stream()` call, text_stream yields direct to UI
- **PDF is UI-only**: not called by LLM, triggered by user button click with gr.Progress()
- **CJK font CSS**: PDF uses `font-family` with macOS/Linux CJK font names; ModelScope needs `setup.sh`
- **No .env in repo**: excluded via `.gitignore`; API key injected as ModelScope env variable in production
- **Pinned deps**: `requirements.txt` has exact versions for reproducible deployment
