import uuid
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from core.config import settings

client = AsyncQdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

async def ensure_collection(vector_size: int):
    exists = await client.collection_exists(settings.qdrant_collection)
    if not exists:
        await client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )
    else:
        info = await client.get_collection(settings.qdrant_collection)
        existing_size = info.config.params.vectors.size
        if existing_size != vector_size:
            raise ValueError(
                f"Qdrant collection vector size mismatch! "
                f"Expected {existing_size}, got {vector_size}. "
                f"Your embedding is the wrong size."
            )


async def upsert_context(text: str, embedding: list[float]):
    await ensure_collection(vector_size=len(embedding))
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={"text": text}
    )
    await client.upsert(
        collection_name=settings.qdrant_collection,
        points=[point]
    )

async def search_context(embedding: list[float], top_k: int = 5) -> list[str]:
    await ensure_collection(vector_size=len(embedding))
    hits = await client.search(
        collection_name=settings.qdrant_collection,
        query_vector=embedding,
        limit=top_k
    )
    return [hit.payload["text"] for hit in hits if hit.payload and "text" in hit.payload]


async def save_embedding_in_qdrant(question: str, answer: str, question_embedding: list[float]):
    """
    Guarda en Qdrant el turno de conversación (pregunta+respuesta) usando el embedding ya generado.
    """
    # Combinar pregunta y respuesta en un texto único para indexar
    combined_text = f"Usuario: {question}\nAsistente: {answer}"

    # Usar el embedding recibido (no volver a generarlo)
    await upsert_context(combined_text, question_embedding)
