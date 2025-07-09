from fastapi import APIRouter, Depends, HTTPException
from db.mongodb import save_chat
from db.models.chats import ChatRequest, ChatResponse
from db.qdrant_client import save_embedding_in_qdrant
from services.rag_chat import retrieve_context
from services.qdrant_chat import retrieve_context_qdrant 
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


        # 1️⃣ Obtener contexto histórico de Mongo
        mongo_context = retrieve_context(
            question=data.question,
            user_id=user_id
        )

        # 2️⃣ Obtener contexto Qdrant + embedding ya generado
        qdrant_context, question_embedding = await retrieve_context_qdrant(
            question=data.question
        )

        # 3️⃣ Combinar ambos contextos
        full_context = (
            f"📌 Historial del usuario:\n{mongo_context}\n\n"
            f"📌 Contexto semántico relevante:\n{qdrant_context}"
        )
        # 2️⃣ Armar prompt con todos los tokens válidos
        prompt = (
            f"Contexto:\n{full_context}\n\n"
            f"OAuth Tokens: {valid_tokens}\n"
            f"Usuario: {data.question}\nAsistente:"
        )

        # 3️⃣ Ejecutar agente
        chatbot = ChatbotAgent(resp['token'])
        agent = chatbot.get_agent()
        async with agent.run_mcp_servers():
            result = await agent.run(prompt)
            # 2️⃣ Guardas en Mongo
            save_chat(
                user_id=user_id,
                question=data.question,
                answer=result.output
            )

            # 3️⃣ Guardas en Qdrant usando el embedding ya calculado
            await save_embedding_in_qdrant(
                question=data.question,
                answer=result.output,
                question_embedding=question_embedding
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error procesando el chat: {str(e)}")

    # 4️⃣ Retornar la respuesta
    return ChatResponse(
        answer=result.output,
        oauth=reauth_urls if reauth_urls else None
    )
