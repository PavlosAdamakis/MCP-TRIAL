# tool_router/tool_router.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def route_command_to_tool(command: str) -> dict:
    """
    Uses GPT to analyze the user's input and return:
    - the tool to run
    - the input data for that tool
    """

    prompt = f"""
You are an agent command router.
Your job is to take any user command and decide which tool to use.

You know the following tools:
- weather: for answering questions like 'weather in Tokyo', 'how hot is it in Athens', or 'is it raining in New York'
- shell: for replying with messages or running commands like 'say hi', 'what time is it', or 'dir'
- store_data: for logging structured info like 'model=GPT4, acc=91%' or 'task=classification, date=today'

Always extract the correct city, country, or place **directly** from the user input — do NOT default to any preset city like Copenhagen.

Your output must be JSON like this:
{{
  "tool": "weather",
  "input": {{"city": "Athens"}}
}}

User: what's the weather in Berlin?
→ {{
  "tool": "weather",
  "input": {{"city": "Berlin"}}
}}

User: accuracy=88, model=SAC
→ {{
  "tool": "store_data",
  "input": {{"text": "accuracy=88, model=SAC"}}
}}

User: tell me something nice
→ {{
  "tool": "shell",
  "input": {{"command": "echo You’re amazing!"}}
}}

Now decide what to do with this command:
\"\"\"{command}\"\"\"
Return only JSON. No explanation.
"""


    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0.2
        )
        raw = response.choices[0].message.content.strip()
        return json.loads(raw)

    except Exception as e:
        return {
            "tool": "shell",
            "input": {"command": f"echo GPT routing failed: {e}"}
        }
