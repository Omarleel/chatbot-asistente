from fastapi import APIRouter, Depends, HTTPException
from db.mongodb import save_chat, get_google_tokens_by_user_id
from db.models.chats import ChatRequest, ChatResponse
from services.rag_chat import retrieve_context
from core.mcp_client import ChatbotAgent
from core.security import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/message", response_model=ChatResponse)
async def chat_with_bot(data:  ChatRequest, resp: dict = Depends(get_current_user)):
    """
    Endpoint para enviar un mensaje al chatbot y guardar la conversación
    """
    # Guardar en Mongo
    try:

        google_access_token = get_google_tokens_by_user_id(resp['user_id'])['access_token']
        context = retrieve_context(question= data.question, user_id=resp['user_id'])
        prompt = (
            f"Contexto:\n{context}\n\n"
            f"google_access_token: {google_access_token}"
            f"Usuario: {data.question}\nAsistente:"
        )
        chatbot = ChatbotAgent(resp['token'])
        agent = chatbot.get_agent()
        async with agent.run_mcp_servers(): 
            result = await agent.run(prompt)
            save_chat(user_id=resp['user_id'], question= data.question, answer=result.output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando en Mongo: {str(e)}")

    # Retornar la respuesta
    return ChatResponse(
        answer=result.output
    )
