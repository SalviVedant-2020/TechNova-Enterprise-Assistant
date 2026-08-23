from graph.graph import graph

while True:

    question = input("\nYou : ")

    if question.lower() in ["exit", "quit", "end"]:

        break

    state = {

        "question": question,

        "route": "",

        "sql_query": "",

        "sql_result": "",

        "sql_error": "",

        "rag_result": "",

        "final_answer": "",

        "retries": 0,
    }

    result = graph.invoke(state)
    print(result)

    print("\nAssistant :\n")

    print(result["final_answer"])