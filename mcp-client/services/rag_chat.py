from db.mongodb import get_recent_chats

def retrieve_context(question: str, user_id: str, top_k: int = 5) -> str:
    # Recientes chats del usuario
    history = get_recent_chats(user_id, limit=top_k)
    formatted_history = "\n".join(
        [f"Usuario: {chat['question']}\nAsistente: {chat['answer']}" for chat in reversed(history)]
    )
    return formatted_history