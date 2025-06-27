import logging
import sys
import faiss
from llama_index.core import (
    SimpleDirectoryReader,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# dimensions of BAAI/bge-small-en-v1.5
d = 384
faiss_index = faiss.IndexFlatL2(d)

# load documents
documents = SimpleDirectoryReader("./Cosmere/Cosmere/").load_data()


vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# save index to disk
index.storage_context.persist()

# load index from disk
vector_store = FaissVectorStore.from_persist_dir("./storage")
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir="./storage"
)
index = load_index_from_storage(storage_context=storage_context)
