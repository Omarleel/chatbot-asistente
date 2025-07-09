from datetime import datetime
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.mcp import MCPServerStreamableHTTP
from httpx import AsyncClient
from core.config import settings

class ChatbotAgent:
    def __init__(self, access_token: str, system_prompt: str = None):
        self.access_token = access_token

        # Setup HTTPX
        self.http_client = AsyncClient(timeout=30)

        # Configurar modelo LLM
        self.model = GroqModel(
            "llama3-70b-8192",
            provider=GroqProvider(
                api_key=settings.groq_api_key,
                http_client=self.http_client
            )
        )

        # Configurar servidor MCP con Authorization
        self.mcp_server = MCPServerStreamableHTTP(
            settings.mcp_server_uri,
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

        # ✅ Si no se pasó system_prompt, usa el por defecto
        if system_prompt is None:
            system_prompt = (
                f"Fecha actual: {datetime.now()}. "
                "Eres un asistente experto que programa reuniones en Google Calendar que se comunica en español. "
                "Debes ser amigable con el usuario e inferir los datos que podrían faltar para llamar a las herramientas. "
                "Para crear eventos debes solicitar al menos el nombre."
            )

        # Crear el Agent
        self.agent = Agent(
            model=self.model,
            mcp_servers=[self.mcp_server],
            system_prompt=system_prompt
        )

    def get_agent(self) -> Agent:
        return self.agent
