from fastapi import APIRouter, Depends, HTTPException
from db.mongodb import save_chat
from db.models.chats import ChatRequest, ChatResponse
from services.rag_chat import retrieve_context
from core.mcp_client import ChatbotAgent
from core.security import get_current_user
from utils.oauth_manager import manage_all_oauth

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/message", response_model=ChatResponse)
async def chat_with_bot(data: ChatRequest, resp: dict = Depends(get_current_user)):
    """
    Endpoint para enviar un mensaje al chatbot y guardar la conversación
    """
    try:
        user_id = resp['_id']

        # 1️⃣ Obtener tokens válidos y URLs de reautorización
        oauth_result = manage_all_oauth(user_id)
        valid_tokens = oauth_result.get("valid_tokens", {})
        reauth_urls = oauth_result.get("reauthorize_urls", {})

        # 2️⃣ Armar prompt con todos los tokens válidos
        context = retrieve_context(question=data.question, user_id=user_id)
        prompt = (
            f"Contexto:\n{context}\n\n"
            f"OAuth Tokens: {valid_tokens}\n"
            f"Usuario: {data.question}\nAsistente:"
        )

        # 3️⃣ Ejecutar agente
        chatbot = ChatbotAgent(resp['token'])
        agent = chatbot.get_agent()
        async with agent.run_mcp_servers():
            result = await agent.run(prompt)
            save_chat(user_id=user_id, question=data.question, answer=result.output)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error procesando el chat: {str(e)}")

    # 4️⃣ Retornar la respuesta
    return ChatResponse(
        answer=result.output,
        oauth=reauth_urls if reauth_urls else None
    )
