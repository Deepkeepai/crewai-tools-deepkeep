# Publishing crewai-tools-deepkeep

Follow these steps to publish the package to PyPI and get it listed in the CrewAI community.

---

## Step 1 — Create a GitHub repository

1. Go to https://github.com/new
2. Name it `crewai-tools-deepkeep`
3. Make it **Public** (required for PyPI discoverability and CrewAI listing)
4. Push the contents of this folder to the repo:
   ```bash
   git init
   git add .
   git commit -m "Initial release v0.1.0"
   git remote add origin https://github.com/gilarel/crewai-tools-deepkeep.git
   git push -u origin main
   ```

---

## Step 2 — Create a PyPI account & API token

1. Register at https://pypi.org/account/register/
2. Once logged in, go to **Account Settings → API tokens**
3. Create a token scoped to this project (or "All projects" for first publish)
4. Save the token — you'll only see it once

---

## Step 3 — Build and publish

Install the build tools:
```bash
pip install build twine
```

Build the distribution:
```bash
cd crewai-tools-deepkeep
python -m build
# Creates dist/crewai_tools_deepkeep-0.1.0.tar.gz
#        dist/crewai_tools_deepkeep-0.1.0-py3-none-any.whl
```

Upload to PyPI:
```bash
twine upload dist/*
# Username: __token__
# Password: pypi-<your token>
```

Verify it's live at: https://pypi.org/project/crewai-tools-deepkeep/

---

## Step 4 — Submit to the CrewAI community showcase

1. Go to https://github.com/crewAIInc/crewAI-tools/issues/new
2. Title: **[Community Tool] crewai-tools-deepkeep — DeepKeep AI Firewall**
3. Include in the body:
   ```
   ## Tool Name
   crewai-tools-deepkeep

   ## PyPI
   https://pypi.org/project/crewai-tools-deepkeep/

   ## GitHub
   https://github.com/gilarel/crewai-tools-deepkeep

   ## Description
   DeepKeep AI Firewall tools for CrewAI agents.
   Check user prompts against safety guardrails, create firewall conversations,
   and call the DeepKeep API — all from within a CrewAI workflow.

   ## Tools included
   - CheckInputTool
   - CreateConversationTool
   - MakeApiCallTool

   ## Install
   pip install crewai-tools-deepkeep
   ```

This gets the tool listed in the official CrewAI tools directory.

---

## Updating the package

1. Bump the version in both `pyproject.toml` and `src/crewai_tools_deepkeep/__init__.py`
2. Commit and push to GitHub
3. Rebuild and re-upload:
   ```bash
   python -m build
   twine upload dist/*
   ```

---

## Optional — GitHub Actions for automated publishing

Create `.github/workflows/publish.yml` to auto-publish on every tagged release:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

Store your PyPI token in **GitHub → Settings → Secrets → PYPI_API_TOKEN**.
Then publish by tagging:
```bash
git tag v0.1.0
git push origin v0.1.0
```
