"""Reply-language directives for assembled system prompts.

The chat UI sends ``X-OpenJarvis-Locale``; CLI / config use
``[system_prompt] language``. A contextvar lets the HTTP header override
the configured language for the current request without mutating shared
config objects.
"""

from __future__ import annotations

from contextvars import ContextVar

_request_language: ContextVar[str] = ContextVar("openjarvis_request_language", default="")

SPANISH_REPLY_DIRECTIVE = (
    "IMPORTANTE: Responde SIEMPRE en español claro y natural, "
    "incluso si el usuario escribe en otro idioma. "
    "Usa un tono cercano y profesional. "
    "No cambies al inglés salvo que el usuario lo pida, "
    "o cites un nombre propio, un comando o un término técnico "
    "que no tenga traducción habitual."
)


def set_request_language(language: str | None) -> None:
    """Bind a per-request locale override (e.g. from X-OpenJarvis-Locale)."""
    _request_language.set((language or "").strip())


def resolve_reply_language(configured: str = "") -> str:
    """Prefer the request override, then the configured language."""
    return _request_language.get() or (configured or "").strip()


def apply_reply_language(prompt: str, language: str | None) -> str:
    """Append a language directive when the resolved locale is Spanish."""
    lang = (language or "").strip().lower()
    if not lang.startswith("es"):
        return prompt
    if "Responde SIEMPRE en español" in prompt or "Responde siempre en español" in prompt:
        return prompt
    if prompt.strip():
        return f"{SPANISH_REPLY_DIRECTIVE}\n\n{prompt.lstrip()}"
    return SPANISH_REPLY_DIRECTIVE
