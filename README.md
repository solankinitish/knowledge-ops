# KnowledgeOps
**Web-grounded multi-hop research engine — live search, hybrid reranking, grounded LLM answer**  
80% pass rate on a complex multi-hop benchmark · Built from first principles
<img width="1568" height="749" alt="image" src="https://github.com/user-attachments/assets/a6663f75-bf0c-4317-8a5e-a973f71d4390" />


![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![RAG](https://img.shields.io/badge/Architecture-RAG-purple)
![Ollama](https://img.shields.io/badge/LLM-Ollama%2FMistral-orange)
![License](https://img.shields.io/badge/MIT-License-lightgrey)

KnowledgeOps is a **web-grounded research engine** built from first principles.  
It searches the live web, retrieves and ranks the most answerable content, and generates grounded answers using a local LLM — without hallucinating.

---

## What This Project Demonstrates

- Building a **multi-hop RAG pipeline from scratch**
- **Answerability-driven retrieval** — not just semantic similarity
- **Hybrid reranking** combining cosine similarity with question-type-aware heuristics
- **Query decomposition** using the LLM itself as a planner
- **Grounding enforcement** to prevent hallucination
- **Systematic pipeline debugging** with full stage-by-stage logging

---

## Features

- **Multi-hop query decomposition** — complex queries broken into independent sub-questions, each retrieved separately
- **Hybrid reranking** — cosine similarity + spaCy answerability scoring weighted by question type (who/when/where vs what/how/why)
- **Grounding enforcement** — LLM answers only from retrieved context, returns "I don't know" otherwise
- **Fault-tolerant extraction** — handles SSL errors, login walls, timeouts, and 403s gracefully
- **Adaptive prompting** — extraction mode for entity questions, explanation mode for descriptive questions
- **Full pipeline logging** — every stage logged for systematic debugging

---

## Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI, Uvicorn |
| Search | DuckDuckGo (ddgs) |
| Extraction | requests, BeautifulSoup |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB (in-memory) |
| NLP | spaCy (en_core_web_sm) |
| LLM | Mistral via Ollama (local) |
| Language | Python 3.11 |

---

## Architecture

```
User Query
│
▼
QueryPlanner       — LLM-based decomposition into sub-questions
│
▼
QueryProcessor     — normalize, rewrite, expand per sub-question
│
▼
SearchEngine       — DuckDuckGo, top 5 URLs after deduplication
│
▼
PageExtractor      — article/main targeting, login-wall detection
│
▼
TextChunker        — 1000 char chunks, min line length 50
│
▼
EmbeddingService   — MiniLM, 384-dim vectors
│
▼
VectorStore        — ChromaDB in-memory
│
▼
VectorRetriever    — Top-10 recall
│
▼
Reranker           — hybrid cosine + spaCy, question-type weights
│
▼
PromptBuilder      — extraction/explanation mode, grounding enforcement
│
▼
OllamaProvider     — Mistral local
│
▼
Answer
```

---

## Retrieval Pipeline
```
User Query
↓
Query Decomposition (QueryPlanner)
↓
Search + Extraction per Sub-question
↓
Chunk + Embed
↓
Vector Recall (Top-10)
↓
Hybrid Reranking (Top-3)
↓
Grounded Prompt → LLM
↓
Answer
```

---

## Example

**Query**
What is FastAPI and who created it?

**Sub-questions (QueryPlanner)**
["What is FastAPI?", "Who created FastAPI?"]

**Retrieved Context**
FastAPI is a modern, high-performance web framework for building APIs
with Python, created by Sebastián Ramírez in December 2018.

**Response**
FastAPI is a modern web framework for building APIs with Python.
It was created by Sebastián Ramírez.

---

## Evaluation

Benchmark of 5 queries covering all question types:

| Query | Type | Result |
|---|---|---|
| Who owns Virgin Group + born when? | who + when | PASS ✅ |
| What is the 2nd Amendment? | what | PASS ✅ |
| When did first person reach Mars? | grounding test | PASS ✅ |
| How to fractionally distillate crude oil? | how | PASS ✅ |
| Why did Bose resign from Congress? | why | PARTIAL ⚠️ |

**Score: 4/5**

---

## Observability

Every stage of the pipeline is logged:

- Sub-questions from QueryPlanner
- URLs collected and processed
- Chunk count per run
- Retrieved chunk content
- Full prompt sent to LLM
- LLM response

This makes systematic debugging possible — any wrong answer can be traced to its exact failure stage without guessing.

---

## How to Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**2. Install Ollama and pull Mistral**
```bash
ollama pull mistral
```

**3. Start the API server**
```bash
uvicorn main:app --reload
```

**4. Run the interactive test**
```bash
python -m scripts.test_research_service
```

**5. Run the evaluation benchmark**
```bash
python -m scripts.evaluate
```

---

## Project Structure
```
knowledge_ops/
├── app/
│   ├── api/            — FastAPI server and routes
│   ├── extraction/     — HTML to text extraction
│   ├── llm/            — Ollama provider and LLM client
│   ├── processing/     — chunker, query processor, query planner
│   ├── prompts/        — prompt builder
│   ├── retrieval/      — embeddings, vector store, retriever, reranker
│   ├── search/         — search engine
│   ├── services/       — research service orchestrator
│   └── utils/          — logger
├── scripts/
│   ├── test_research_service.py
│   └── evaluate.py
├── main.py
├── requirements.txt
└── .gitignore
```

---

## Known Limitations

- **Source reliability** — results vary by run depending on which URLs DuckDuckGo returns and which succeed
- **Heuristic reranker** — rule-based spaCy scoring, a learned cross-encoder would be significantly stronger
- **In-memory vector store** — ChromaDB resets on every run, no persistence across sessions
- **LLM latency** — Ollama/Mistral averages 10-40s per query, not production-ready
- **Grounding enforcement** — prompt-based only; programmatic cosine similarity verification removed due to semantic mismatch between synthesized answers and raw chunks
- **QueryPlanner non-determinism** — LLM output format varies between runs; dict normalization applied as defensive fix

---

## Summary

KnowledgeOps demonstrates a **production-style web-grounded RAG engine** combining live web search, multi-hop query decomposition, hybrid answerability-driven reranking, grounding enforcement, and local LLM inference — built and understood from first principles.
