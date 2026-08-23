from pathlib import Path

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from tools.sql_tools import get_table_names
from utils.config import settings


llm = ChatGroq(
    model=settings.LLM_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=0,
)


# ==========================================
# Dynamic SQL Tables
# ==========================================

sql_tables = "\n".join(
    f"- {table}"
    for table in get_table_names()
)


# ==========================================
# Dynamic Company Documents
# ==========================================

docs_dir = Path(__file__).resolve().parent.parent / "documents"

documents = "\n".join(
    f"- {pdf.stem.replace('_', ' ')}"
    for pdf in docs_dir.glob("*.pdf")
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the routing agent for TechNova's Enterprise AI Assistant.

Your ONLY job is to decide which node should answer the user's question.

Return EXACTLY ONE of these words.

SQL
RAG
HYBRID
NO_TOOL

==================================================
ASSISTANT SCOPE
==================================================

This assistant ONLY answers questions related to TechNova.

Questions outside TechNova should ALWAYS return:

NO_TOOL

==================================================
AVAILABLE SQL DATA
==================================================

The SQL database contains these tables:

{tables}

Use SQL ONLY if the database alone can answer the question.

==================================================
AVAILABLE COMPANY DOCUMENTS
==================================================

The document knowledge base contains:

{documents}

Use RAG ONLY if the documents alone can answer the question.

==================================================
ROUTING RULES
==================================================

SQL

Use SQL when ONLY structured database information is required.

Examples:

- Who has the highest salary?
- List all employees.
- Show active projects.
- Show attendance for Juan Green.
- Which department has the highest average salary?

----------------------------------------

RAG

Use RAG when ONLY company documents or policies are required.

Examples:

- Explain the promotion policy.
- What is the leave policy?
- Explain the WFH policy.
- Explain the employee handbook.

----------------------------------------

HYBRID

Use HYBRID whenever BOTH database information AND company policies are required.

Typical examples:

- Can Juan Green be promoted?
- Is Steven Campbell eligible for promotion?
- Who all are eligible for promotion?
- Who qualifies for reimbursement?
- Can Rahul work from home?
- Who satisfies the leave policy?
- which employee has leave left
- how many leaves rahul has ?

If the question asks whether someone satisfies a company policy,
ALWAYS choose HYBRID.

When uncertain between SQL and HYBRID,

ALWAYS choose HYBRID.

----------------------------------------

NO_TOOL

Use NO_TOOL for:

- Greetings
- Small talk
- Jokes
- Questions outside TechNova
- Questions unrelated to the available database or company documents

Examples:

- Hello
- Tell me a joke.
- What is the population of India?
- Who won yesterday's cricket match?
- Explain Binary Search.

Return ONLY ONE WORD.

SQL

RAG

HYBRID

NO_TOOL
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


planner_chain = prompt | llm


def planner(state):

    route = (
        planner_chain.invoke(
            {
                "question": state["question"],
                "tables": sql_tables,
                "documents": documents,
            }
        )
        .content
        .strip()
        .upper()
    )

    if route not in {"SQL", "RAG", "HYBRID", "NO_TOOL"}:
        route = "NO_TOOL"

    return {
        "route": route
    }