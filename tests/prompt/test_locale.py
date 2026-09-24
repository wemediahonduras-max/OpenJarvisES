from openjarvis.core.config import SystemPromptConfig
from openjarvis.prompt.builder import SystemPromptBuilder
from openjarvis.prompt.locale import (
    SPANISH_REPLY_DIRECTIVE,
    apply_reply_language,
    resolve_reply_language,
    set_request_language,
)


def test_apply_reply_language_spanish_appends_directive():
    prompt = apply_reply_language("You are OpenJarvis.", "es")
    assert "You are OpenJarvis." in prompt
    assert SPANISH_REPLY_DIRECTIVE in prompt


def test_apply_reply_language_english_is_noop():
    assert apply_reply_language("You are OpenJarvis.", "en") == "You are OpenJarvis."


def test_apply_reply_language_is_idempotent():
    once = apply_reply_language("Hola.", "es-MX")
    assert apply_reply_language(once, "es") == once


def test_request_override_beats_configured_language():
    set_request_language("es")
    try:
        assert resolve_reply_language("en") == "es"
    finally:
        set_request_language("")


def test_builder_appends_spanish_from_config():
    builder = SystemPromptBuilder(
        agent_template="You are OpenJarvis.",
        system_prompt_config=SystemPromptConfig(language="es"),
    )
    prompt = builder.build()
    assert "You are OpenJarvis." in prompt
    assert "Responde SIEMPRE en español" in prompt
