from pathlib import Path

from langchain_community.vectorstores import FAISS

from langchain_community.retrievers import BM25Retriever

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.rrf import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.vectorstore = FAISS.load_local(
            str(base_dir / "vectorstore" / "faiss_index"),
            embeddings,
            allow_dangerous_deserialization=True,
        )

        self.faiss = self.vectorstore.as_retriever(
            search_kwargs={"k":5}
        )

        documents = []

        docs_dir = base_dir / "documents"

        for pdf in docs_dir.glob("*.pdf"):

            loader = PyPDFLoader(str(pdf))

            documents.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )

        chunks = splitter.split_documents(documents)

        self.bm25 = BM25Retriever.from_documents(chunks)

        self.bm25.k = 5

    def retrieve(self, query):

        semantic = self.faiss.invoke(query)

        keyword = self.bm25.invoke(query)

        fused = reciprocal_rank_fusion(
            semantic,
            keyword,
        )

        return fused