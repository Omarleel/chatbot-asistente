from fastmcp import Client
from core.config import settings

class MCPClient:
    def __init__(self):
        self.server_url = settings.mcp_server_uri

    async def list_tools(self):
         async with Client(self.server_url) as client:
            tools = await client.list_tools()
            return list(tools.keys())
            
    async def call_tool(self, tool_name: str, payload: dict) -> dict:
        """
        Se conecta al servidor MCP y llama a la herramienta indicada con el payload dado.
        
        Args:
            tool_name: Nombre registrado de la herramienta MCP.
            payload: Diccionario con los argumentos de la herramienta.
        
        Returns:
            Respuesta de la herramienta (diccionario).
        """
        async with Client(self.server_url) as client:
            result = await client.call_tool(tool_name, payload)
            return result
