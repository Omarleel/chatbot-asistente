from fastmcp import FastMCP
from tools import google_calendar, slack

mcp = FastMCP(name="chatbot-asistente")

# REGISTRAR TODAS LAS TOOLS
google_calendar.register(mcp)
slack.register(mcp)