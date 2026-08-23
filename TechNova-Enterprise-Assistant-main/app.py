import streamlit as st

from graph.graph import graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TechNova Enterprise Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 TechNova Enterprise Assistant")
st.caption(
    "LangGraph • Hybrid RAG (FAISS + BM25 + RRF) • SQL Agent"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "workflows" not in st.session_state:
    st.session_state.workflows = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Project")

    st.write(
        """
TechNova Enterprise Assistant

• LangGraph

• Hybrid RAG

• SQL Agent

• SQLite

• FAISS

• BM25

• Reciprocal Rank Fusion
"""
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.session_state.workflows = []

        st.rerun()


# ============================================================
# DISPLAY OLD CHAT
# ============================================================

for i, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            workflow = st.session_state.workflows[i // 2]

            with st.expander("🔍 Agent Workflow"):

                route = workflow["route"]

                if route == "SQL":
                    st.success("Planner Route : SQL")

                elif route == "RAG":
                    st.info("Planner Route : RAG")

                elif route == "HYBRID":
                    st.warning("Planner Route : HYBRID")

                else:
                    st.error("Planner Route : NO_TOOL")

                st.subheader("Generated SQL")

                if workflow["sql_query"]:
                    st.code(
                        workflow["sql_query"],
                        language="sql",
                    )
                else:
                    st.info("SQL Worker not used.")

                st.subheader("Retrieved Context")

                if workflow["rag_result"]:
                    st.text(workflow["rag_result"])
                else:
                    st.info("RAG Worker not used.")

                st.subheader("SQL Result")

                if workflow["sql_result"]:
                    st.code(workflow["sql_result"])
                else:
                    st.info("No SQL Result.")

                st.subheader("Retries")

                st.write(workflow["retries"])

                if workflow["sql_error"]:

                    st.subheader("SQL Error")

                    st.error(workflow["sql_error"])


# ============================================================
# USER INPUT
# ============================================================

question = st.chat_input(
    "Ask anything about TechNova..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

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

    with st.spinner("Thinking..."):

        result = graph.invoke(state)

    answer = result["final_answer"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.session_state.workflows.append(result)

    with st.chat_message("assistant"):

        st.write(answer)

        with st.expander("🔍 Agent Workflow"):

            route = result["route"]

            if route == "SQL":
                st.success("Planner Route : SQL")

            elif route == "RAG":
                st.info("Planner Route : RAG")

            elif route == "HYBRID":
                st.warning("Planner Route : HYBRID")

            else:
                st.error("Planner Route : NO_TOOL")

            st.subheader("Generated SQL")

            if result["sql_query"]:
                st.code(
                    result["sql_query"],
                    language="sql",
                )
            else:
                st.info("SQL Worker not used.")

            st.subheader("Retrieved Context")

            if result["rag_result"]:
                st.text(result["rag_result"])
            else:
                st.info("RAG Worker not used.")

            st.subheader("SQL Result")

            if result["sql_result"]:
                st.code(result["sql_result"])
            else:
                st.info("No SQL Result.")

            st.subheader("Retries")

            st.write(result["retries"])

            if result["sql_error"]:

                st.subheader("SQL Error")

                st.error(result["sql_error"])