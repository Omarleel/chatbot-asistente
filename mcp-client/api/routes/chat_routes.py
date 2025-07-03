from fastapi import APIRouter, HTTPException
from db.mongodb import save_chat
from db.models.chats import ChatRequest, ChatResponse
from services.rag_chat import retrieve_context
from core.mcp_client import agent

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/message", response_model=ChatResponse)
async def chat_with_bot(data: ChatRequest):
    """
    Endpoint para enviar un mensaje al chatbot y guardar la conversación
    """
    # Guardar en Mongo
    try:

        context = retrieve_context(question= data.question, user_id=data.user_id)
        prompt = (
            f"Contexto:\n{context}\n\n"
            f"Usuario: {data.question}\nAsistente:"
        )
        async with agent.run_mcp_servers(): 
            result = await agent.run(prompt)
            save_chat(user_id=data.user_id, question= data.question, answer=result.output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando en Mongo: {str(e)}")

    # Retornar la respuesta
    return ChatResponse(
        answer=result.output
    )
