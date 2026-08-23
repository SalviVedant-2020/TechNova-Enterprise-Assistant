from typing import TypedDict


class AgentState(TypedDict):

    question: str

    route: str

    sql_query: str

    sql_result: str

    sql_error: str

    rag_result: str

    final_answer: str

    retries: int