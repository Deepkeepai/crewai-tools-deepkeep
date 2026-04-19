"""
CheckInputTool — verify a user prompt against a DeepKeep firewall.

Endpoint:
  POST /v2/firewalls/{firewallId}/conversation/{conversationId}/check_user_input
  Body: { "content": "<text>", "logs": <bool> }

The tool returns the raw API response as a JSON string so that downstream
agents can decide whether to block, warn, or pass the input.
"""

import json
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .auth import get_base_url, get_headers


class CheckInputInput(BaseModel):
    firewall_id: str = Field(
        ...,
        description="The ID of the DeepKeep firewall to check the input against.",
    )
    conversation_id: str = Field(
        ...,
        description="The ID of the conversation the message belongs to.",
    )
    content: str = Field(
        ...,
        description="The user prompt or text content to be checked by the firewall.",
    )
    logs: bool = Field(
        False,
        description=(
            "Set to True to return the full list of detected violations. "
            "Useful for audit or debugging; defaults to False."
        ),
    )


class CheckInputTool(BaseTool):
    name: str = "deepkeep_check_input"
    description: str = (
        "Check a user prompt or AI-generated text against a DeepKeep AI firewall. "
        "Returns a JSON object with violation details. Use this before passing "
        "any user input to an LLM to enforce guardrails and safety policies."
    )
    args_schema: Type[BaseModel] = CheckInputInput

    def _run(
        self,
        firewall_id: str,
        conversation_id: str,
        content: str,
        logs: bool = False,
    ) -> str:
        url = (
            f"{get_base_url()}/v2/firewalls/{firewall_id}"
            f"/conversation/{conversation_id}/check_user_input"
        )
        response = requests.post(
            url,
            headers=get_headers(),
            json={"content": content, "logs": logs},
            timeout=30,
        )
        response.raise_for_status()
        # Wrap under "results" to mirror the Make.com / n8n shape.
        return json.dumps({"results": response.json()}, indent=2)
