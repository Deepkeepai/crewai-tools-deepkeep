"""
CreateConversationTool — open a new conversation inside a DeepKeep firewall.

Endpoint:
  POST /v2/firewalls/{firewallId}/conversation
  Body: {}  (empty JSON object — required by the API even when empty)

Returns the conversation object as a JSON string.  The conversation ID in
the response is what you pass to CheckInputTool on subsequent calls.
"""

import json
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .auth import get_base_url, get_headers


class CreateConversationInput(BaseModel):
    firewall_id: str = Field(
        ...,
        description="The ID of the DeepKeep firewall in which to create the conversation.",
    )


class CreateConversationTool(BaseTool):
    name: str = "deepkeep_create_conversation"
    description: str = (
        "Create a new conversation inside a DeepKeep AI firewall. "
        "Returns a JSON object containing the conversation ID, which must be "
        "passed to deepkeep_check_input for every message in that conversation."
    )
    args_schema: Type[BaseModel] = CreateConversationInput

    def _run(self, firewall_id: str) -> str:
        url = f"{get_base_url()}/v2/firewalls/{firewall_id}/conversation"

        # The DeepKeep API requires a JSON body even when it's empty; sending
        # an empty dict causes some HTTP clients to drop the body, so we send
        # the literal string "{}" with an explicit Content-Type header.
        headers = get_headers()
        response = requests.post(
            url,
            headers=headers,
            data="{}",          # literal empty JSON body — do NOT use json={}
            timeout=30,
        )
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
