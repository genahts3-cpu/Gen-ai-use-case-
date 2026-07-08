# ============================================================
# agent.py - Autonomous Coding Agent for Policy Renewal Agent
# ============================================================

import json
import re
from pathlib import Path
from langchain_openai import ChatOpenAI
import httpx

# ============================================================
# CONFIGURATION
# ============================================================

API_KEY = "sk-_58eVef-ywwIJ1ApjsxRlA"   # <-- replace with your valid key
BASE_URL = "https://genailab.tcs.in/v1"
MODEL_NAME = "genailab-maas-gpt-5.2-codex"

WORKSPACE_PATH = Path(r"C:\Users\GenAICHNKPRUSR04\Documents\CodeAgent")
WORKSPACE_PATH.mkdir(parents=True, exist_ok=True)

# ============================================================
# EDGE BROWSER CONTEXT
# ============================================================

edge_all_open_tabs = [
    {"pageTitle":"Gen-ai-use-case-/Prompt at main · genahts3-cpu/Gen-ai-use-case-","pageUrl":"https://github.com/genahts3-cpu/Gen-ai-use-case-/blob/main/Prompt","tabId":2004287325,"isCurrent":True},
    {"pageTitle":"Internet Security by Zscaler","pageUrl":"https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fgenahts3-cpu%2FGen-ai-use-case-%2Frefs%2Fheads%2Fmain%2FPolicy_Renewal_Agent_Architecture.docx","tabId":2004287357,"isCurrent":False},
    {"pageTitle":"AWS Authentication","pageUrl":"http://127.0.0.1/index.html","tabId":2004287368,"isCurrent":False},
    {"pageTitle":"genahts3-cpu/Gen-ai-use-case-","pageUrl":"https://github.com/genahts3-cpu/Gen-ai-use-case-","tabId":2004287360,"isCurrent":False},
    {"pageTitle":"Buy Credits | Claude Platform","pageUrl":"https://platform.claude.com/buy_credits","tabId":2004287341,"isCurrent":False},
    {"pageTitle":"Building a multi-agent insurance platform - Claude","pageUrl":"https://claude.ai/chat/6c2ac3c5-a380-4734-94a0-4ffe302443ab","tabId":2004287349,"isCurrent":False},
    {"pageTitle":"New chat - Claude","pageUrl":"https://claude.ai/new","tabId":2004287365,"isCurrent":False},
    {"pageTitle":"ChatGPT","pageUrl":"https://chatgpt.com","tabId":2004287344,"isCurrent":False},
    {"pageTitle":"chat gpt - Search","pageUrl":"https://www.bing.com/search","tabId":2004287300,"isCurrent":False}
]

active_tab = next(tab['pageTitle'] for tab in edge_all_open_tabs if tab['isCurrent'])
other_tabs = [tab['pageTitle'] for tab in edge_all_open_tabs if not tab['isCurrent']]

# ============================================================
# PROMPT TEMPLATE (Policy Renewal Agent)
# ============================================================

CODING_AGENT_PROMPT = f"""
You are a Principal Software Architect and Senior Full Stack Engineer.

Your task is to build a COMPLETE, production-quality, hackathon-ready application.

DO NOT generate code snippets.
Generate an ENTIRE repository.
The repository must be runnable without additional coding.

Context:
Active tab: {active_tab}
Other tabs: {other_tabs}

Respond ONLY with valid JSON in the format:
{{
  "subtasks": [...],
  "files": [{{"path": "...", "content": "..."}}],
  "commands": [...]
}}
"""

# ============================================================
# INITIALIZE LLM
# ============================================================

client = httpx.Client(verify=False)

llm = ChatOpenAI(
    base_url=BASE_URL,
    model=MODEL_NAME,
    api_key=API_KEY,
    http_client=client
)

# ============================================================
# HELPER: Extract JSON from text
# ============================================================

def extract_json(raw_text: str) -> str:
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("No JSON object found in response")

# ============================================================
# FUNCTION: Write files from LLM output
# ============================================================

def write_files_from_response(response_content):
    try:
        text_blocks = [block["text"] for block in response_content if block.get("type") == "text"]
        if not text_blocks:
            print("⚠️ No text block found in response.")
            return

        raw_json = text_blocks[0]
        json_str = extract_json(raw_json)
        data = json.loads(json_str)

        if "subtasks" in data:
            print("Subtasks received:")
            for st in data["subtasks"]:
                print(f" • {st}")

        if "files" in data:
            for f in data["files"]:
                relative_path = Path(f["path"].replace("\\", "/"))
                file_path = WORKSPACE_PATH / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as out:
                    out.write(f["content"])
                print(f"✅ Wrote {file_path}")
        else:
            print("⚠️ No 'files' key in response JSON.")

    except Exception as e:
        print("❌ Failed to parse/write files:", str(e))

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("================================================")
    print("TESTING POLICY RENEWAL AGENT PROMPT")
    print("================================================")

    response = llm.invoke(CODING_AGENT_PROMPT)
    print("Raw LLM Response:\n", response.content)

    write_files_from_response(response.content)
