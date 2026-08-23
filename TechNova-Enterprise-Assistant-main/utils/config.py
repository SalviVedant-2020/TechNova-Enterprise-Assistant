from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    LLM_MODEL = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

    VECTOR_DB_PATH = "vectorstore"

    DATABASE_PATH = "database/company.db"

    DOCUMENT_PATH = "documents"


settings = Settings()