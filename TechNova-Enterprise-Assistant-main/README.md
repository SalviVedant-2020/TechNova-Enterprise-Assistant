# 🤖 TechNova Enterprise Assistant

An AI-powered enterprise assistant built using **LangGraph**, **LangChain**, **Hybrid Retrieval-Augmented Generation (Hybrid RAG)** and a **SQL Agent**.

The assistant intelligently determines whether a user's question should be answered using:

- 📊 Enterprise SQL Database
- 📚 Company Knowledge Base
- 🔀 Both (Hybrid Retrieval + SQL)

and orchestrates the workflow using **LangGraph**.

---

# ✨ Features

- 🧠 LangGraph multi-agent workflow
- 🛣️ Intelligent Planner Agent
- 🗄️ SQL Agent for structured enterprise data
- 📚 Hybrid Retrieval
  - FAISS Semantic Search
  - BM25 Keyword Search
  - Reciprocal Rank Fusion (RRF)
- 🔄 Automatic SQL retry mechanism
- 📝 Answer Synthesizer
- 💬 Streamlit Chat Interface
- 🏢 SQLite enterprise database with synthetic data generated using Faker
- 📄 Enterprise policy documents as knowledge base

---

# 🏗️ Workflow

```text
                           User Question
                                 │
                                 ▼
                         Planner Agent
                                 │
          ┌──────────────┬──────────────┬──────────────┬──────────────┐
          │              │              │              │
         SQL            RAG          HYBRID        NO_TOOL
          │              │              │              │
          │              │              ▼              ▼
          │              │       Retrieve Policies   General Chat
          │              │              │
          │              │              ▼
          │              │       Generate SQL
          │              │              │
          │              │              ▼
          │              │       Execute SQL
          │              │              │
          │              │     SQL Execution Error?
          │              │              │
          │              │      Yes ────┴──── No
          │              │       │
          │              │ Retry SQL Generation
          │              │   (Maximum 2 retries)
          └──────────────┴──────────────┘
                                 │
                                 ▼
                        Answer Synthesizer
                                 │
                                 ▼
                           Final Response
```

---

# 🧠 Hybrid Retrieval Flow

Unlike a traditional SQL-first approach, hybrid questions follow this workflow:

```text
User Question
      │
      ▼
Retrieve Relevant Company Policies (RAG)
      │
      ▼
Generate SQL using Retrieved Policy
      │
      ▼
Execute SQL
      │
      ▼
Combine Policy + SQL Results
      │
      ▼
Generate Final Answer
```

For example:

> **Who is eligible for promotion?**

The assistant first retrieves the promotion policy from the knowledge base, then generates SQL using those business rules before producing the final answer.

---

# 📂 Project Structure

```text
TechNova-Enterprise-Assistant/

├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
│
├── database/
│   └── company.db
│
├── documents/
│
├── graph/
│
├── nodes/
│
├── scripts/
│   ├── create_database.py
│   ├── create_documents.py
│   └── ingest_documents.py
│
├── tools/
│   ├── hybrid_retriever.py
│   └── sql_tools.py
│
├── utils/
│   ├── config.py
│   ├── rrf.py
│   └── sql_utils.py
│
└── vectorstore/
    ├── index.faiss
    └── index.pkl
```

---

# ⚙️ Tech Stack

### AI & Orchestration

- LangGraph
- LangChain
- Groq LLM

### Retrieval

- FAISS
- BM25
- Reciprocal Rank Fusion (RRF)
- HuggingFace Embeddings

### Database

- SQLite

### Frontend

- Streamlit

### Other Libraries

- Faker
- SQLAlchemy
- Pydantic

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/TechNova-Enterprise-Assistant.git

cd TechNova-Enterprise-Assistant
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy the example file:

### Windows

```bash
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

---

## 5. (Optional) Regenerate Resources

The repository already includes:

- SQLite database
- Vector store
- Enterprise documents

If you wish to regenerate them:

Create the database:

```bash
python scripts/create_database.py
```

Create enterprise documents:

```bash
python scripts/create_documents.py
```

Rebuild the vector store:

```bash
python scripts/ingest_documents.py
```

---

## 6. Run the Application

### Streamlit Interface

```bash
streamlit run app.py
```

### Terminal Interface

```bash
python main.py
```

---

# 💬 Example Questions

### SQL

- Who has the highest salary?
- List all employees in Engineering.
- Show employees currently on leave.

### RAG

- Explain the promotion policy.
- What is the company's leave policy?
- Explain the employee code of conduct.

### Hybrid

- Who is eligible for promotion?
- Which employees satisfy the promotion policy?
- Find employees meeting the leave policy requirements.

---

# 🔮 Future Improvements

- Conversation memory
- Authentication
- Source document citations
- Multi-document upload
- Docker support
- Cloud deployment
- Multi-database support

---

# 👨‍💻 Author

**Aman Kumar**

GitHub: https://github.com/Aman-Kumar2002

LinkedIn: https://www.linkedin.com/in/mraman-kumar

---

# 📄 License

This project is licensed under the MIT License.