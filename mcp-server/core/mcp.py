from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider
from tools import google_calendar, slack
from pathlib import Path

# ✅ Cargar clave pública
PUBLIC_KEY = Path("public_key.pem").read_text()
# ✅ Configurar auth
auth = BearerAuthProvider(
    public_key=PUBLIC_KEY,
    issuer="https://example.com",
    audience="mi-mcp-server"
)

# ✅ Crear FastMCP con autenticación
mcp = FastMCP(
    name="chatbot-asistente",
    auth=auth
)

# ✅ Registrar todas las tools
google_calendar.register(mcp)
slack.register(mcp)