"""
DeepKeep API authentication helpers.

Credentials are read from environment variables:
  DEEPKEEP_SUBDOMAIN  – your tenant subdomain (e.g. "acme")
  DEEPKEEP_API_KEY    – your API key

Both are required.  Raise clear errors when missing so users know exactly
what to set rather than getting a cryptic HTTP 401.
"""

import os


def get_base_url() -> str:
    """Return the base API URL for the configured tenant."""
    subdomain = os.environ.get("DEEPKEEP_SUBDOMAIN", "").strip()
    if not subdomain:
        raise EnvironmentError(
            "DEEPKEEP_SUBDOMAIN is not set. "
            "Export it as the subdomain of your DeepKeep instance "
            "(e.g. export DEEPKEEP_SUBDOMAIN=acme)."
        )
    return f"https://api.{subdomain}.deepkeep.ai/api"


def get_headers() -> dict:
    """Return the auth + content-type headers required by every request."""
    api_key = os.environ.get("DEEPKEEP_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError(
            "DEEPKEEP_API_KEY is not set. "
            "Export it as your DeepKeep API key "
            "(e.g. export DEEPKEEP_API_KEY=dk_…)."
        )
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
