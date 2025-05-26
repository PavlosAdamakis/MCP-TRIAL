# tools/excel.py

import pandas as pd
import os


def run_excel_tool(inputs):
    """
    Cleans and optionally filters an Excel file based on a user's instruction.
    Returns a result summary string and (optional) preview HTML.
    """
    filepath = inputs.get("filepath")
    instructions = inputs.get("command", "")

    if not filepath or not os.path.exists(filepath):
        return " Couldn't find the uploaded Excel file.", ""

    try:
        df = pd.read_excel(filepath)
        actions_taken = []

        # Casual terms mapping to real actions
        instr = instructions.lower()

        if any(word in instr for word in ["clean", "tidy", "fix"]):
            df.dropna(how="all", inplace=True)
            df.dropna(axis=1, how="all", inplace=True)
            actions_taken.append("removed empty rows and columns")

        if "strip headers" in instr:
            df.columns = [str(col).strip() for col in df.columns]
            actions_taken.append("stripped column headers")

        if "sort by" in instr:
            for word in instr.split():
                if word in df.columns:
                    df.sort_values(by=word, inplace=True)
                    actions_taken.append(f"sorted by '{word}'")
                    break

        # Filtering (e.g., "only beer")
        for keyword in ["beer", "wine"]:
            if f"only {keyword}" in instr:
                df = df[df["Category"].str.lower() == keyword]
                actions_taken.append(f"filtered to only {keyword.title()} entries")

        # Save cleaned file
        cleaned_path = "cleaned_data.xlsx"
        df.to_excel(cleaned_path, index=False)

        summary = "File cleaned. " + ", ".join(actions_taken).capitalize() + ".\nDownload: [click here](/download)"
        return summary, ""

    except Exception as e:
        return f" Failed to process Excel file: {e}", ""
