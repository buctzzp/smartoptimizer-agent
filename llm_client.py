import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

_API_KEY = None
_BASE_URL = None
_MODEL = None
_CLIENT = None


def _load_config():
    global _API_KEY, _BASE_URL, _MODEL
    if _API_KEY is not None:
        return
    _API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    _BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
    _MODEL = os.getenv("ANTHROPIC_MODEL", "deepseek-chat")


def get_client() -> Anthropic:
    global _CLIENT
    _load_config()
    if _CLIENT is None:
        _CLIENT = Anthropic(api_key=_API_KEY, base_url=_BASE_URL)
    return _CLIENT


def get_model() -> str:
    _load_config()
    return _MODEL


def get_api_key() -> str | None:
    _load_config()
    return _API_KEY
