# agents/your_agent.py

from mcp.protocol import Message
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load your OpenAI API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class YourAgent:
    def __init__(self, name, mcp, user_agent):
        self.name = name
        self.mcp = mcp
        self.user = user_agent  # Reference to the WebUser
        mcp.register(self)

    def receive(self, message):
        print(f"🧠 {self.name} received a message from {message.sender}")

        # Extract what the user typed
        user_text = message.content.get("text", "")

        # Ask GPT to turn that into a tool request
        tool_request = self.convert_text_to_tool_input(user_text)

        # Build a new message for OpsAgent to actually run the tool
        task_msg = Message(
            sender=self.name,
            receiver="OpsAgent",
            performative="run_tool",
            content=tool_request
        )
        self.mcp.dispatch(task_msg)

    def convert_text_to_tool_input(self, user_input: str) -> dict:
        """Ask GPT to figure out which tool to use and what input to give it."""

        prompt = f"""
You are a smart assistant that turns user requests into tool instructions.

Tools available:
- weather: expects input like {{ "city": "Berlin" }}
- shell: expects input like {{ "command": "echo Hello" }}
- excel: expects input like {{ "filepath": "uploaded_x.xlsx", "instructions": "drop empty rows" }}
- store_data: expects input like {{ "text": "model=BERT, accuracy=92%" }}

Respond only with JSON. No extra explanation.

User said:
\"\"\"{user_input}\"\"\"
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{ "role": "user", "content": prompt }],
                temperature=0.2
            )

            raw_json = response.choices[0].message.content.strip()
            return json.loads(raw_json)

        except Exception as e:
            print(f"⚠️ GPT failed to parse: {e}")
            return {
            "tool": "shell",
            "input": {
            "command": f"echo Sorry! I hit a limit or error: {str(e)[:100]}"
        }
    }
