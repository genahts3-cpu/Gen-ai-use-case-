import json
import re
from pathlib import Path
import httpx
from langchain_openai import ChatOpenAI
import asyncio

PROMPT_TEMPLATE = """You are a Principal Software Architect and Senior Full Stack Engineer.

Build a COMPLETE, production-ready, runnable application based on the user's request below.

User Request: {user_prompt}

Rules:
- Generate the ENTIRE repository, not snippets
- Every file must be complete and runnable as-is
- Include requirements.txt or package.json as needed
- Include a README.md with setup instructions

Respond ONLY with valid JSON (no markdown, no explanation outside JSON):
{{
  "app_name": "...",
  "description": "...",
  "subtasks": ["step 1", "step 2"],
  "files": [
    {{"path": "relative/path/file.py", "content": "full file content here"}}
  ],
  "commands": ["pip install -r requirements.txt", "python main.py"]
}}"""


def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        pass
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("Could not extract valid JSON from LLM response")


async def run_agent(api_key: str, user_prompt: str, workspace: str, base_url: str, model: str):
    workspace_path = Path(workspace)
    workspace_path.mkdir(parents=True, exist_ok=True)

    yield f"data: 🔧 Connecting to model: {model}\n\n"
    await asyncio.sleep(0)

    try:
        http_client = httpx.Client(verify=False)
        llm = ChatOpenAI(
            base_url=base_url,
            model=model,
            api_key=api_key,
            http_client=http_client,
            timeout=120,
        )
    except Exception as e:
        yield f"data: ❌ Failed to initialize LLM: {e}\n\n"
        return

    yield "data: 📡 Sending request to LLM (this may take 30-60s)...\n\n"
    await asyncio.sleep(0)

    try:
        prompt = PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        response = await asyncio.get_event_loop().run_in_executor(None, llm.invoke, prompt)
        raw = response.content
        # Handle case where content is a list of blocks (new OpenAI API format)
        if isinstance(raw, list):
            raw = next((b["text"] for b in raw if isinstance(b, dict) and b.get("type") == "text"), "")
    except Exception as e:
        yield f"data: ❌ LLM call failed: {e}\n\n"
        return

    yield f"data: 📥 Response received ({len(raw)} chars). Parsing...\n\n"
    await asyncio.sleep(0)

    try:
        data = _extract_json(raw)
    except Exception as e:
        yield f"data: ❌ JSON parse error: {e}\n\n"
        yield f"data: 📄 Raw preview: {raw[:500]}\n\n"
        return

    yield f"data: 🚀 App: {data.get('app_name', 'generated-app')}\n\n"
    await asyncio.sleep(0)

    desc = data.get("description", "")
    if desc:
        yield f"data: 📝 {desc}\n\n"
        await asyncio.sleep(0)

    for i, st in enumerate(data.get("subtasks", []), 1):
        yield f"data: 📌 {i}. {st}\n\n"
        await asyncio.sleep(0)

    files = data.get("files", [])
    if not files:
        yield "data: ⚠️ No files were generated. Try a more specific prompt.\n\n"
        return

    yield f"data: 📁 Writing {len(files)} files to: {workspace_path}\n\n"
    await asyncio.sleep(0)

    written = []
    for f in files:
        try:
            rel = Path(f["path"].replace("\\", "/"))
            fp = workspace_path / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(f["content"], encoding="utf-8")
            written.append(str(rel))
            yield f"data: ✅ {rel}\n\n"
            await asyncio.sleep(0)
        except Exception as e:
            yield f"data: ❌ Failed to write {f.get('path')}: {e}\n\n"
            await asyncio.sleep(0)

    for cmd in data.get("commands", []):
        yield f"data: 💡 $ {cmd}\n\n"
        await asyncio.sleep(0)

    yield f"data: 🎉 Done! {len(written)} files written to {workspace_path}\n\n"
    yield "data: __DONE__\n\n"
