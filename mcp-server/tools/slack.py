def register(mcp):
    @mcp.tool()
    def add(a: int, b: int) -> str:
        """Adds two numbers together."""
        return f"La suma es {a + b}"
