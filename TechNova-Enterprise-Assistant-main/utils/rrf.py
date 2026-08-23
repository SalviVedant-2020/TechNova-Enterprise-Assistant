def reciprocal_rank_fusion(*rankings, k=60):

    scores = {}

    docs = {}

    for ranking in rankings:

        for rank, doc in enumerate(ranking):

            key = doc.page_content

            docs[key] = doc

            scores.setdefault(key, 0)

            scores[key] += 1 / (k + rank + 1)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        docs[key]
        for key, _ in ranked
    ]