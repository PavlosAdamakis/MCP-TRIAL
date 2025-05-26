from mcp.protocol import Message

class OpsAgent:
    def __init__(agent, name, mcp, tools=None):
        agent.name = name
        agent.mcp = mcp
        agent.tools = tools or {}  # Dictionary of tool functions
        agent.mcp.register(agent)  # Register with the MCP server

    def receive(agent, message):
        print(f"{agent.name} received: {message}")

        if message.performative == "run_tool":
            tool_name = message.content.get("tool")
            tool_input = message.content.get("input", {})

            tool_fn = agent.tools.get(tool_name)
            if tool_fn:
                try:
                    tool_result = tool_fn(tool_input)

                    # Check if the result is a tuple (used by Excel tool)
                    if isinstance(tool_result, tuple) and len(tool_result) == 2:
                        result, preview_html = tool_result
                    else:
                        result = tool_result
                        preview_html = ""

                except Exception as e:
                    result = f" Error running tool: {e}"
                    preview_html = ""
            else:
                result = f" Tool '{tool_name}' not found."
                preview_html = ""

            # Send back the result
            response = Message(
                sender=agent.name,
                receiver=message.sender,
                performative="tool_result",
                content={"result": result, "html": preview_html}
            )
            agent.mcp.dispatch(response)
