"""
MakeApiCallTool — perform an arbitrary authenticated request to the DeepKeep API.

This is an escape-hatch for endpoints not yet covered by dedicated tools.
The agent supplies the URL path, HTTP method, optional headers / query params,
and an optional JSON body string.  Auth headers are injected automatically.

Returns a JSON string with { statusCode, headers, body } — matching the shape
used by the Make.com and n8n integrations.
"""

import json
from typing import Optional, Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .auth import get_base_url, get_headers


class MakeApiCallInput(BaseModel):
    path: str = Field(
        ...,
        description=(
            "The API path relative to deepkeep.ai/api, e.g. '/v2/firewalls'. "
            "Leading slash is optional."
        ),
    )
    method: str = Field(
        "GET",
        description="HTTP method: GET, POST, PUT, or DELETE.",
    )
    query_params: Optional[dict] = Field(
        None,
        description="Optional dictionary of URL query-string parameters.",
    )
    extra_headers: Optional[dict] = Field(
        None,
        description=(
            "Optional extra request headers. Auth headers are already injected "
            "automatically — do not include X-API-Key here."
        ),
    )
    body: Optional[str] = Field(
        None,
        description=(
            "Optional raw request body (usually a JSON string). "
            "Leave empty for GET / DELETE requests that have no body."
        ),
    )


class MakeApiCallTool(BaseTool):
    name: str = "deepkeep_make_api_call"
    description: str = (
        "Perform any authenticated HTTP request to the DeepKeep API. "
        "Use this for endpoints not covered by the dedicated tools. "
        "Returns a JSON object with statusCode, headers, and body."
    )
    args_schema: Type[BaseModel] = MakeApiCallInput

    def _run(
        self,
        path: str,
        method: str = "GET",
        query_params: Optional[dict] = None,
        extra_headers: Optional[dict] = None,
        body: Optional[str] = None,
    ) -> str:
        # Normalize path — strip leading slashes to avoid double-slash in URL.
        clean_path = path.lstrip("/")
        url = f"{get_base_url()}/{clean_path}"

        headers = get_headers()
        if extra_headers:
            headers.update(extra_headers)

        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=query_params or {},
            data=body or None,
            timeout=30,
        )

        # Try to parse the response body as JSON for downstream convenience.
        try:
            parsed_body = response.json()
        except ValueError:
            parsed_body = response.text

        return json.dumps(
            {
                "statusCode": response.status_code,
                "headers": dict(response.headers),
                "body": parsed_body,
            },
            indent=2,
        )
