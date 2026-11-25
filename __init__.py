"""onomeo provider profile for Hermes Agent.

Registers onomeo (https://onomeo.com) as a provider over its
OpenAI-compatible Chat Completions endpoint. Credential resolution, the
``/model`` picker, ``hermes doctor`` and the ``--provider`` flag all wire up
from the provider registry, so this plugin touches no core files.

Model ids are bare (``deepseek-v4.1-flash``, ``claude-sonnet-5.5``,
``gpt-6.2-sol`` …). The live catalog comes from
``GET https://onomeo.com/v1/models`` with the user's key; ``fallback_models``
is only shown when that catalog is unreachable.
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any

from providers import register_provider
from providers.base import ProviderProfile

logger = logging.getLogger(__name__)

PROVIDER_ID = "onomeo"
API_KEY_ENV = "ONOMEO_API_KEY"
BASE_URL_ENV = "ONOMEO_BASE_URL"
BASE_URL = "https://onomeo.com/v1"
VERSION = "0.1.0"


def _supported_kwargs(cls: type, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Drop profile fields the installed Hermes build does not define.

    Passing a field an older build lacks raises ``TypeError`` at import, which
    the plugin loader swallows, so the provider would silently fail to
    register. Filtering to the fields this build knows degrades gracefully.
    """
    try:
        known = {field.name for field in dataclasses.fields(cls)}
    except TypeError:  # pragma: no cover - non-dataclass profile base
        return dict(kwargs)
    dropped = sorted(set(kwargs) - known)
    if dropped:
        logger.debug("onomeo: this Hermes build has no profile field(s) %s, skipping", ", ".join(dropped))
    return {key: value for key, value in kwargs.items() if key in known}


PROFILE_FIELDS: dict[str, Any] = {
    "name": PROVIDER_ID,
    "aliases": ("onomeo-ai",),
    "display_name": "onomeo",
    "description": "onomeo: one OpenAI-compatible key for Claude, GPT, Gemini, DeepSeek, Kimi and GLM",
    "signup_url": "https://onomeo.com/dashboard",
    "env_vars": (API_KEY_ENV, BASE_URL_ENV),
    "base_url": BASE_URL,
    "hostname": "onomeo.com",
    "auth_type": "api_key",
    "api_mode": "chat_completions",
    # Identifies Hermes Agent traffic in onomeo's per-tool usage counts.
    "default_headers": {"User-Agent": f"HermesAgent-onomeo/{VERSION}"},
    # New accounts can call this model for free within daily limits; it also
    # suits compression and title generation.
    "default_aux_model": "deepseek-v4.1-flash",
    # Shown only when the live catalog is unreachable; every id was live-tested.
    "fallback_models": (
        "deepseek-v4.1-flash",
        "claude-sonnet-5.5",
        "claude-opus-5.5",
        "claude-haiku-5.5",
        "gpt-6.2-sol",
        "gemini-4-argon",
        "kimi-k3",
        "glm-5.3",
    ),
}

onomeo = ProviderProfile(**_supported_kwargs(ProviderProfile, PROFILE_FIELDS))

register_provider(onomeo)
