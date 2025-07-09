from sentence_transformers import SentenceTransformer
from db.qdrant_client import search_context

embedding_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
def generate_embedding(text: str) -> list[float]:
    embedding = embedding_model.encode(text)
    return embedding.tolist()

async def retrieve_context_qdrant(question: str, top_k: int = 5) -> tuple[str, list[float]]:
    """
    Recupera contexto relevante desde Qdrant y retorna el embedding generado.
    Returns:
        semantic_context (str): Los textos relevantes encontrados en Qdrant.
        question_embedding (list[float]): El embedding generado para la pregunta.
    """
    # ✅ 1️⃣ Generar embedding con SentenceTransformer
    question_embedding = generate_embedding(question)

    # ✅ 2️⃣ Buscar en Qdrant
    semantic_chunks = await search_context(question_embedding, top_k=top_k)
    semantic_context = "\n".join(semantic_chunks)

    return semantic_context, question_embedding
