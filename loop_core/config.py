import os

# EMBEDDINGS
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 384))

# LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.5-turbo")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# FAISS
FAISS_INDEX_PATH = "faiss.index"

# RETRIEVAL
TOP_K_CANDIDATES = 100
FINAL_TOP_K = 5

# RRF
RRF_K = 5

# RANKING
RECENCY_WEIGHT = 0.2



