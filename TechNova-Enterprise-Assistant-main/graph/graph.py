from langgraph.graph import StateGraph, END

from graph.state import AgentState

from nodes.planner import planner
from nodes.sql_worker import sql_worker
from nodes.rag_worker import rag_worker
from nodes.synthesizer import synthesizer
from nodes.chat_worker import chat_worker


# =====================================================
# ROUTE AFTER PLANNER
# =====================================================

def route_question(state):
    return state["route"]


# =====================================================
# ROUTE AFTER RAG
# =====================================================

def after_rag(state):

    if state["route"] == "HYBRID":
        return "sql"

    return "synthesizer"


# =====================================================
# ROUTE AFTER SQL
# =====================================================

def after_sql(state):

    # Retry SQL if execution failed
    if state.get("sql_error", "") != "":

        if state.get("retries", 0) < 2:
            return "retry"

        return "failed"

    return "synthesizer"


# =====================================================
# BUILD GRAPH
# =====================================================

builder = StateGraph(AgentState)

builder.add_node("planner", planner)
builder.add_node("rag_worker", rag_worker)
builder.add_node("sql_worker", sql_worker)
builder.add_node("synthesizer", synthesizer)
builder.add_node("chat_worker", chat_worker)

builder.set_entry_point("planner")


# =====================================================
# PLANNER ROUTING
# =====================================================

builder.add_conditional_edges(
    "planner",
    route_question,
    {
        "SQL": "sql_worker",
        "RAG": "rag_worker",
        "HYBRID": "rag_worker",
        "NO_TOOL": "chat_worker",
    },
)


# =====================================================
# RAG ROUTING
# =====================================================

builder.add_conditional_edges(
    "rag_worker",
    after_rag,
    {
        "sql": "sql_worker",
        "synthesizer": "synthesizer",
    },
)


# =====================================================
# SQL ROUTING
# =====================================================

builder.add_conditional_edges(
    "sql_worker",
    after_sql,
    {
        "retry": "sql_worker",
        "synthesizer": "synthesizer",
        "failed": END,
    },
)


# =====================================================
# END
# =====================================================

builder.add_edge(
    "chat_worker",
    END,
)

builder.add_edge(
    "synthesizer",
    END,
)


graph = builder.compile()