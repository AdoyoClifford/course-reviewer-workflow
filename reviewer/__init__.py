from vertexai.preview import reasoning_engines
from .agent import root_agent


# Define the app for the ADK
app = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)

__all__ = ["app"]