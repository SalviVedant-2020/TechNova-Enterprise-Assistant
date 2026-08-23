from tools.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()

query = "What is the promotion policy?"

docs = retriever.retrieve(query)

print(f"\nRetrieved {len(docs)} documents\n")

for i, doc in enumerate(docs, start=1):

    print("=" * 70)
    print(f"Document {i}")
    print("=" * 70)

    print("Metadata:")
    print(doc.metadata)

    print("\nContent:")
    print(doc.page_content)
    print()