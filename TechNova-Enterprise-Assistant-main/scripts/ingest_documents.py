from pathlib import Path
import pickle

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from rank_bm25 import BM25Okapi



BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

VECTORSTORE_DIR.mkdir(exist_ok=True)



print("=" * 50)
print("Loading PDFs...")
print("=" * 50)



documents = []

for pdf in DOCUMENTS_DIR.glob("*.pdf"):

    loader = PyPDFLoader(str(pdf))

    docs = loader.load()

    documents.extend(docs)



print(f"Loaded {len(documents)} pages.")



# =====================================================
# CHUNKING
# =====================================================

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=100,

)

chunks = text_splitter.split_documents(documents)

print(f"Generated {len(chunks)} chunks.")
# =====================================================
# EMBEDDINGS
# =====================================================

print("=" * 50)
print("Creating Embeddings...")
print("=" * 50)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# =====================================================
# CREATE FAISS
# =====================================================

print("=" * 50)
print("Building FAISS...")
print("=" * 50)

vectorstore = FAISS.from_documents(
    chunks,
    embeddings,
)

vectorstore.save_local(
    str(VECTORSTORE_DIR / "faiss_index")
)

print("FAISS Saved.")

print("=" * 50)
print("Knowledge Base Ready")
print("=" * 50)