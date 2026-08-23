from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from utils.config import settings


llm = ChatGroq(
    model=settings.LLM_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=0.1,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are TechNova's Enterprise AI Assistant.

Answer the user's question ONLY using the information provided.

You may receive:

1. SQL Query
   - Shows how the database was queried.

2. SQL Result
   - Contains factual data retrieved from the database.

3. Company Policy / Document Context
   - Contains company rules and business policies.

IMPORTANT

If the SQL query already applies business rules
(for example rating >= 4.5, training_completed = TRUE,
experience >= 3 years),

DO NOT ask for those values again.

Assume the SQL result already satisfies those conditions.

If some policy conditions cannot be verified from the database
(for example HR approval or business requirements),
clearly mention that.

Guidelines

• Never invent facts.
• Never invent policy.
• Use SQL results as facts.
• Use company policy as business rules.
• Combine both naturally.
• Be concise and professional.
"""
        ),
        (
            "human",
            """
Question

{question}


Executed SQL

{sql_query}


SQL Result

{sql_result}


Company Policy

{rag_result}
"""
        ),
    ]
)

chain = prompt | llm


def synthesizer(state):

    response = chain.invoke(
        {
            "question": state["question"],
            "sql_query": state.get("sql_query", ""),
            "sql_result": state.get("sql_result", ""),
            "rag_result": state.get("rag_result", ""),
        }
    )

    return {
        "final_answer": response.content
    }