"""
crewai-tools-deepkeep
=====================
DeepKeep AI Firewall tools for CrewAI agents.

Available tools
---------------
- CheckInputTool          – check a prompt against a firewall's guardrails
- CreateConversationTool  – open a new firewall conversation
- MakeApiCallTool         – arbitrary authenticated request to the DeepKeep API

Quick start
-----------
    import os
    os.environ["DEEPKEEP_SUBDOMAIN"] = "acme"
    os.environ["DEEPKEEP_API_KEY"]   = "dk_..."

    from crewai_tools_deepkeep import CheckInputTool, CreateConversationTool

    agent = Agent(
        role="AI Firewall Guard",
        tools=[CreateConversationTool(), CheckInputTool()],
        ...
    )
"""

from .check_input import CheckInputTool
from .create_conversation import CreateConversationTool
from .make_api_call import MakeApiCallTool

__all__ = [
    "CheckInputTool",
    "CreateConversationTool",
    "MakeApiCallTool",
]

__version__ = "0.1.0"
