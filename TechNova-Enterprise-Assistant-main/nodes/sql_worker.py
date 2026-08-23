from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from tools.sql_tools import get_schema
from tools.sql_tools import execute_sql

from utils.config import settings


llm = ChatGroq(
    model=settings.LLM_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=0,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert SQLite developer.

Your ONLY job is to generate a valid SQLite query.

You are given:

1. Database Schema
2. Relevant Company Policy (may be empty)
3. User Question
4. Previous SQL Error (if any)

The company policy contains business rules.

Use those business rules whenever they are relevant.

Examples:

If policy says:

Promotion requires
- 3 years experience
- Rating >= 4.5
- Training completed

then generate SQL that retrieves or filters using those conditions whenever possible.

IMPORTANT RULES

- Return ONLY SQL.
- Never explain.
- Never use markdown.
- Never use ```sql.
- Never invent tables or columns.
- Use ONLY the provided schema.
- If previous SQL failed, correct your query.

Database Schema

{schema}

Relevant Company Policy

{rag_context}

Previous SQL Error

{error}
"""
        ),
        (
            "human",
            "{question}"
        ),
    ]
)

chain = prompt | llm


def sql_worker(state):

    schema = get_schema()

    rag_context = state.get("rag_result", "")

    previous_error = state.get("sql_error", "")

    response = chain.invoke(
        {
            "schema": schema,
            "rag_context": rag_context,
            "question": state["question"],
            "error": previous_error,
        }
    ).content.strip()

    sql = (
        response
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    success, result = execute_sql(sql)

    if success:

        return {

            "sql_query": sql,

            "sql_result": result,

            "sql_error": "",

        }

    return {

        "sql_query": sql,

        "sql_result": "",

        "sql_error": result,

        "retries": state["retries"] + 1,

    }