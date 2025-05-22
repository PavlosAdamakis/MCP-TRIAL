class Message:
    def __init__(agent, sender, receiver, performative, content):
        agent.sender = sender
        agent.receiver = receiver
        agent.performative = performative
        agent.content = content

    def __repr__(agent):
        return f"[{agent.performative.upper()}] {agent.sender} → {agent.receiver}: {agent.content}"


class FastMCP:
    def __init__(agent_server):
        agent_server.registry = {}

    def register(agent_server, agent):
        agent_server.registry[agent.name] = agent

    def dispatch(agent_server, message):
        receiver = agent_server.registry.get(message.receiver)
        if receiver:
            receiver.receive(message)
        else:
            print(f"Agent {message.receiver} not found.")
