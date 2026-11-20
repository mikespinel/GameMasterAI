from datapizza.core.vectorstore import (
    VectorConfig,
)
from datapizza.vectorstores.qdrant import (
    QdrantVectorstore,
)

from rag.config import (
    COLLECTION_NAME,
)


def create_vectorstore():

    return QdrantVectorstore(
        host="localhost",
        port=6333,
    )



def ensure_collection():

    store = QdrantVectorstore(
        host="localhost",
        port=6333,
    )

    collections = store.get_collections()

    if COLLECTION_NAME not in collections:

        store.create_collection(
            collection_name=COLLECTION_NAME,
            vector_config=[
                VectorConfig(
                    name="text_embedding",
                    dimensions=1536,
                )
            ]
        )

    return store