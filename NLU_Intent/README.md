# Agent 2: NLU & Intent Detection - Runbook

This guide covers the end-to-end process to run the **Industrial Grade** NLU and Intent Detection Agent, including native `pgvector` semantic search and session persistence.

---

## 📋 Prerequisites

1. **Python 3.10+** (with `pip`)
2. **Node.js 18+** (with `npm`)
3. **PostgreSQL 15+** (Installed and running)
4. **Visual Studio Build Tools** (Required for compiling `pgvector` on Windows)

---

## 🛠️ Step 1: Install `pgvector` on Windows

`pgvector` must be compiled manually on Windows. Follow these exact steps:

1. **Open "x64 Native Tools Command Prompt for VS"** as Administrator.
2. **Set your Postgres path**:
   ```powershell
   set "PGROOT=C:\Program Files\PostgreSQL\18"  # Replace with your actual version/path
   ```
3. **Download and Build**:
   ```powershell
   git clone --branch v0.7.4 https://github.com/pgvector/pgvector.git
   cd pgvector
   nmake
   nmake install
   ```
4. **Enable the Extension**:
   Log in to your Postgres database and run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

---

## 📦 Step 2: Install Project Dependencies

1. **Python Virtual Environment**:

   ```powershell
   cd "Agents/NLU_Intent"
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Node/Prisma Dependencies**:
   ```powershell
   npm install
   ```

---

## 🗄️ Step 3: Initialize Database & Schema

1. **Configure Environment**:
   Ensure your `.env` file has the correct `DATABASE_URL` and `GROQ_API_KEY`.

2. **Push Prisma Schema**:
   This creates the native vector tables and indexes.

   ```powershell
   npx prisma db push
   ```

3. **Seed Q&A Pairs with Embeddings**:
   This script generates 384-dimensional embeddings for the 90 Q&A pairs and stores them in Postgres.
   ```powershell
   python prisma/seed_vectors.py
   ```

---

## 🚀 Step 4: Run the Agent

Start the FastAPI server:

```powershell
uvicorn nlu_service.app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔍 Step 5: Test & Output

You can verify the semantic search using the provided test script:

```powershell
python verify_search.py
```

### Expected Output Format

When you call the `/analyze` endpoint:

- **Input**: User utterance (e.g., "how do I book a flat?").
- **Process**:
  1. Agent (Groq) detects the intent and extracts entities.
  2. NLU engine performs an matching search against 90 vectors in PostgreSQL using native SQL-level cosine distance.
  3. Session history is automatically saved to the `session_storage` table.
- **Output**: A JSON object containing the `intent`, `entities`, and the best matched `answer_text` from the knowledge base.

---

_Created for the Real-Estate Agent Workflow._
