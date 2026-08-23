from tools.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()


def rag_worker(state):

    docs = retriever.retrieve(state["question"])

    # Only keep the top few most relevant chunks.
    docs = docs[:3]

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return {
        "rag_result": context
    }