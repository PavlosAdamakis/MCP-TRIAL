import pandas as pd
import os

EXCEL_FILE = "agent_data.xlsx"

def run_store_data_tool(params: dict) -> str:
    raw_text = params.get("text", "")
    try:
        # Convert input to dict from key=value format
        data = {}
        for pair in raw_text.split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                data[key.strip()] = value.strip()

        if not data:
            return "⚠️ No valid key=value data found."

        # Load existing or create new
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
        else:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return "✅ Data stored successfully in Excel."
    except Exception as e:
        return f"❌ Failed to store data: {e}"
