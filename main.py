from mcp.protocol import FastMCP, Message
from agents.ops_agent import OpsAgent
from tools.shell import run_shell_tool

# Step 1: Create the message router (MCP server)
mcp = FastMCP()

# Step 2: Register the agent that can run tools
tools = {
    "shell": run_shell_tool
}
ops_agent = OpsAgent(name="OpsAgent", mcp=mcp, tools=tools)

# Step 3: Create a dummy agent to send a test message
class DummyAgent:
    def __init__(agent, name, mcp):
        agent.name = name
        agent.mcp = mcp
        agent.mcp.register(agent)

    def receive(agent, message):
        print(f"{agent.name} got response: {message.content['result']}")

dummy = DummyAgent(name="Tester", mcp=mcp)

# Step 4: Send a tool request from the dummy agent to the OpsAgent
msg = Message(
    sender="Tester",
    receiver="OpsAgent",
    performative="run_tool",
    content={
        "tool": "shell",
        "input": {"command": "echo Hello Agent"}
    }
)

# Step 5: Send it through the MCP network
mcp.dispatch(msg)
