from datetime import datetime
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.mcp import MCPServerStreamableHTTP
from httpx import AsyncClient
from core.config import settings


ahora = datetime.now()
año = ahora.year
mes = ahora.month
dia = ahora.day
# Setup Groq + HTTPX
http_client = AsyncClient(timeout=30)
model = GroqModel(
    "llama3-70b-8192",
    provider=GroqProvider(api_key=settings.groq_api_key, http_client=http_client),
)

# 🧠 Agente con servidor MCP usando streamable HTTP
mcp_server = MCPServerStreamableHTTP(settings.mcp_server_uri)
#

agent = Agent(
    model=model,
    mcp_servers=[mcp_server],
    system_prompt="Eres un asistente que ayuda a programar reuniones y enviar notificaciones vía herramientas remotas."
)
