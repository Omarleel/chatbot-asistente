from core.mcp import mcp
if __name__ == "__main__":
    # mcp.run(transport="stdio")
    # mcp.run(transport="sse")
    mcp.run(transport="streamable-http")

