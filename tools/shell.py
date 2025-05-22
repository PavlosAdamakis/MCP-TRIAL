import subprocess

def run_shell_tool(params: dict) -> str:
    command = params.get("command")

    if not command:
        return " No command provided."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output or " Command ran but returned no output."
    except Exception as e:
        return f" Error running command: {e}"
