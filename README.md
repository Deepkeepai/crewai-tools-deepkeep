# crewai-tools-deepkeep

**DeepKeep AI Firewall tools for CrewAI agents.**

Add real-time LLM security and guardrails to your CrewAI workflows. These tools let any CrewAI agent interact with the [DeepKeep](https://deepkeep.ai) AI Firewall API — checking prompts against safety policies, creating tracked conversations, or making arbitrary authenticated API calls.

---

## Installation

```bash
pip install crewai-tools-deepkeep
```

---

## Configuration

Set two environment variables before running your crew:

```bash
export DEEPKEEP_SUBDOMAIN="acme"      # Your DeepKeep tenant subdomain
export DEEPKEEP_API_KEY="dk_..."      # Your DeepKeep API key
```

---

## Available Tools

| Tool | Description |
|------|-------------|
| `CheckInputTool` | Check a user prompt against a firewall's guardrails |
| `CreateConversationTool` | Open a new tracked conversation in a firewall |
| `MakeApiCallTool` | Perform any authenticated request to the DeepKeep API |

---

## Usage

### Basic — guard an agent's input

```python
import os
from crewai import Agent, Task, Crew
from crewai_tools_deepkeep import CheckInputTool, CreateConversationTool

os.environ["DEEPKEEP_SUBDOMAIN"] = "acme"
os.environ["DEEPKEEP_API_KEY"]   = "dk_..."

FIREWALL_ID = "your-firewall-id"

guard_agent = Agent(
    role="AI Security Guard",
    goal="Ensure all user inputs comply with company AI policies before they reach other agents.",
    backstory="You are a security specialist responsible for enforcing AI guardrails.",
    tools=[CreateConversationTool(), CheckInputTool()],
    verbose=True,
)

check_task = Task(
    description=(
        f"1. Create a new conversation in firewall '{FIREWALL_ID}'.\n"
        f"2. Check the following user input against it:\n\n"
        f"   'How do I reset my password?'\n\n"
        f"3. Return whether the input was flagged and why."
    ),
    expected_output="A JSON summary of the firewall check result.",
    agent=guard_agent,
)

crew = Crew(agents=[guard_agent], tasks=[check_task])
result = crew.kickoff()
print(result)
```

### Advanced — escape hatch for any API endpoint

```python
from crewai_tools_deepkeep import MakeApiCallTool

tool = MakeApiCallTool()

# List all firewalls
result = tool._run(path="/v2/firewalls/search", method="POST", body='{"query":[]}')
print(result)
```

---

## Tool Reference

### `CheckInputTool`

Check a user prompt against a DeepKeep firewall.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `firewall_id` | `str` | ✅ | ID of the firewall |
| `conversation_id` | `str` | ✅ | ID of the conversation (from `CreateConversationTool`) |
| `content` | `str` | ✅ | The text to check |
| `logs` | `bool` | ❌ | Return full violation list (default: `False`) |

**Returns:** JSON string with `{ "results": { ... } }` containing violation details.

---

### `CreateConversationTool`

Open a new conversation in a DeepKeep firewall.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `firewall_id` | `str` | ✅ | ID of the firewall |

**Returns:** JSON string with the new conversation object, including its `id`.

---

### `MakeApiCallTool`

Perform any authenticated HTTP request to the DeepKeep API.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `str` | ✅ | API path, e.g. `/v2/firewalls` |
| `method` | `str` | ❌ | HTTP method (default: `GET`) |
| `query_params` | `dict` | ❌ | URL query parameters |
| `extra_headers` | `dict` | ❌ | Additional headers (auth is injected automatically) |
| `body` | `str` | ❌ | Raw request body (usually a JSON string) |

**Returns:** JSON string with `{ "statusCode", "headers", "body" }`.

---

## Contributing

Issues and pull requests are welcome at [github.com/Deepkeepai/crewai-tools-deepkeep](https://github.com/Deepkeepai/crewai-tools-deepkeep).

## License

MIT © [DeepKeep](https://deepkeep.ai)
