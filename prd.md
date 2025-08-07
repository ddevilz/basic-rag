### 1. Introduction

#### 1.1 Project Goal
[cite_start]The goal of this project is to design and implement an **LLM-Powered Intelligent Query-Retrieval System** that can process large documents and make contextual decisions[cite: 9]. [cite_start]This system will handle real-world scenarios in domains like insurance, legal, HR, and compliance[cite: 10]. The solution will be built using **LangChain**.

---

### 2. System Requirements

#### 2.1 Functional Requirements

**Input:**
* [cite_start]The system must process documents in PDF, DOCX, and email formats[cite: 12].
* [cite_start]It needs to handle policy/contract data efficiently[cite: 13].
* [cite_start]It must be able to parse natural language queries[cite: 14].

**Processing:**
* The system will use **LangChain** for its components.
* [cite_start]It must utilize embeddings (**FAISS/Pinecone**) for semantic search[cite: 16].
* [cite_start]The system must implement clause retrieval and matching based on semantic similarity[cite: 17, 39].
* [cite_start]The architecture will include an **LLM Parser** to extract structured queries [cite: 32, 33][cite_start], an **Embedding Search** component [cite: 35, 36][cite_start], a **Clause Matching** component [cite: 38, 39][cite_start], and a **Logic Evaluation** component for decision processing[cite: 45, 46].
* [cite_start]It needs to provide an explainable decision rationale[cite: 18].

**Output:**
* [cite_start]The system must output structured JSON responses[cite: 19, 48].

---

### 3. Technical Specifications

* **Recommended Tech Stack (with additions):**
    * [cite_start]**Backend:** FastAPI [cite: 110, 111]
    * [cite_start]**Vector DB:** Pinecone [cite: 112, 113]
    * [cite_start]**LLM:** GPT-4 [cite: 114, 115]
    * [cite_start]**Database:** PostgreSQL [cite: 116, 117]
    * **Framework:** LangChain

* **API Documentation:**
    * [cite_start]**Base URL:** `http://localhost:8000/api/v1` [cite: 73]
    * [cite_start]**Authentication:** `Authorization: Bearer 97d9f7fb0dd56082c8776bb5be7a4ae27a39ec2121fcb7ed89277aa49dcefda1` [cite: 75]
    * [cite_start]**Endpoint:** `POST /hackrx/run` to run submissions[cite: 78, 79, 80].

---

### 4. Evaluation and Scoring

#### 4.1 Evaluation Parameters
The solution will be evaluated based on:
* [cite_start]**Accuracy:** Precision of query understanding and clause matching[cite: 53, 54].
* [cite_start]**Token Efficiency:** Optimized LLM token usage and cost-effectiveness[cite: 58, 59].
* [cite_start]**Latency:** Response speed and real-time performance[cite: 60, 61].
* [cite_start]**Reusability:** Code modularity and extensibility[cite: 62, 63].
* [cite_start]**Explainability:** Clear decision reasoning and clause traceability[cite: 69, 70].

#### 4.2 Scoring System
[cite_start]The scoring system is indicative and may vary[cite: 157].
* **Document-Level Weightage:**
    * [cite_start]**Known Documents** (publicly available) have a low weightage (e.g., 0.5)[cite: 125, 128].
    * [cite_start]**Unknown Documents** (private & unseen) have a high weightage (e.g., 2.0)[cite: 126, 130].
* [cite_start]**Question-Level Weightage:** Each question may have its own weight based on complexity or importance[cite: 132, 133].
* [cite_start]**Score Calculation:** The score for a correct answer is calculated as `Score = Question Weight x Document Weight`[cite: 135, 136]. [cite_start]The final score is the sum of all such scores[cite: 137].
* **Key Points:**
    * [cite_start]Correct answers from unknown documents contribute more to the score[cite: 149].
    * [cite_start]High-weight questions significantly boost the score[cite: 150].
    * [cite_start]Incorrect or unattempted questions contribute 0 to the score[cite: 151].