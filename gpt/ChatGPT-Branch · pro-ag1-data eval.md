# Branch · pro-ag1-data eval

**Created:** 9/6/2025 13:04:12  
**Updated:** 9/6/2025 13:11:17  
**Exported:** 9/6/2025 13:15:24  
**Link:** [https://chatgpt.com/c/68bc6933-2540-8332-9e23-77c1cbf7a8db](https://chatgpt.com/c/68bc6933-2540-8332-9e23-77c1cbf7a8db)  

## Prompt:
Prompt (Final Version for Multiple Options + Interview-Oriented)
You are a senior AI engineer experienced with LangGraph, MCP (tool standardization), A2A (Agent-to-Agent), multiple vector databases (Pinecone/Weaviate/FAISS), chain-of-thought prompting (CoT), in-context learning (ICL), and multi-agent pipelines.
I am a recent CS master’s graduate preparing for job applications. The job requirements I’ve seen mention these technologies, but my current experience is limited to building a simple RAG system with LangChain. To strengthen my resume, I want to design and implement a project that incorporates these technologies.
Please help me:
Provide multiple different project options (at least 3) that highlight the required technologies.
For each option, explain how interviewers will perceive this project — specifically, how it demonstrates mastery of the listed technologies.
For each project, show clearly how the following are applied: LangGraph, MCP, A2A, multiple vector databases (Pinecone/Weaviate/FAISS), CoT/ICL, and multi-agent pipelines.
For each project, provide both:
A Complete Plan (full version showing the ambitious scope).
An MVP Plan (a minimal but working version that can be done quickly to demonstrate the core technologies).
Provide a step-by-step roadmap for both the MVP and the full version。
Provide resume wording suggestions for how I can present each project to highlight the required technical skills.
Important: provide text explanations only, do not include any code examples.

## Response:
Request for GPT-5 Pro

Reasoned for 5m 14s

Below are **four** interview‑ready project options (each with a Complete Plan and an MVP Plan, step‑by‑step roadmaps, and resume bullets). Every option explicitly shows how you’ll apply **LangGraph, MCP (tool standardization), A2A (Agent‑to‑Agent), Pinecone/Weaviate/FAISS, CoT/ICL, and multi‑agent pipelines**.

> **How to use this:** Pick one project and build the MVP first to get a working demo, then extend toward the Complete Plan. Each option is crafted to make your skills obvious to interviewers, with concrete discussion points and outcomes.

* * *

Option 1 — **Policy & Audit Copilot**
-------------------------------------

_A multi‑agent system that answers compliance questions (SOC 2, ISO 27001, GDPR), maps controls to evidence, and assembles audit packets._

### Why interviewers will love it

*   Demonstrates **vendor‑agnostic retrieval** across three vector backends and **routing trade‑offs** (cost vs. latency vs. filterability).
*   Shows **standards thinking** via MCP: one tool contract, many interchangeable implementations (cloud file stores, data catalogs, PII scanners).
*   Clear **A2A**: an _Auditor Agent_ debates an _Org Security Agent_ to converge on evidence and gaps.
*   **LangGraph** makes the orchestration legible (graph of Planner → Router → Specialists → Assembler).
*   Mature **reasoning hygiene**: you’ll talk about CoT/ICL design, structured scratchpads, and leakage controls.

### Where each required tech shows up

*   **LangGraph:**  
    Nodes: _Intake/Planner_, _Retrieval Router_, _Policy Mapper_, _Evidence Collector_, _Gap‑Analysis Critic_, _Report Assembler_.  
    Edges: `needs_context`, `route_by_domain`, `evidence_found`, `needs_review`, `finalize_report`.
*   **MCP (tool standardization):**  
    MCP servers for: `documents.search`, `drive.get` (evidence), `pii.scan`, `ticket.create` (Jira), `controls.catalog` (standard control texts). One schema, pluggable backends.
*   **A2A:**  
    _Auditor Agent_ ↔ _Org Security Agent_ message types: `CLAIM`, `EVIDENCE_REQUEST`, `COUNTEREVIDENCE`, `RISK_RATING`, `RESOLUTION`. Negotiation converges on status per control.
*   **Vector DBs:**
    *   **Pinecone** — large, long‑tail corpora of policies/runbooks (managed scale, ANN).
    *   **Weaviate** — hybrid search and strict metadata filters (e.g., `framework=SOC2`, `owner=IT`).
    *   **FAISS** — local/offline cache for session‑specific chunks and rapid re‑ranking.  
        A **retrieval router** learns which backend to hit based on query shape, filter needs, and latency budget.
*   **CoT/ICL:**  
    A “control‑mapping exemplars bank” (ICL) + structured reasoning fields (claims, evidence, gaps). Use high‑level rationales captured as JSON (avoid dumping raw chain‑of‑thought).
*   **Multi‑agent pipeline:**  
    Planner → Retriever(s) → Policy Mapper → Evidence Collector → Critic → Assembler, with an _Auditor_ vs _Org_ agent debate loop.

### MVP Plan (minimal but working)

**Goal:** Answer “Show me evidence for SOC 2 CC6.1” and produce a 1‑page audit summary.

1.  Prepare a small corpus (policies, a few tickets, mock evidence PDFs).
2.  Build **FAISS** local index for the corpus; build **Pinecone** index for the same; add **Weaviate** with basic metadata (`doc_type`, `framework`).
3.  Implement an **MCP `documents.search`** tool that can hit any of the three backends via a `backend` parameter.
4.  Create a **LangGraph** with nodes: _Planner_ → _Retrieval Router_ → _Policy Mapper_ → _Assembler_.
5.  Hardcode a simple **router heuristic** (if filter present → Weaviate; if “policy” keywords → Pinecone; else FAISS+rerank).
6.  Add a basic **A2A** exchange: _Auditor Agent_ requests evidence, _Org Security Agent_ responds from retrieval results.
7.  Add **ICL** exemplars for 3–5 control mappings and a structured reasoning schema (claims/evidence/gaps).
8.  CLI demo: user query → control mapping → evidence list → summary page.

**MVP Roadmap (step‑by‑step)**

*   Collect corpus → chunk & embed → create three indices → MCP server for `documents.search` → LangGraph skeleton → router heuristic → two agents (Auditor/Org) with a minimal message schema → assemble a PDF/markdown audit summary.

### Complete Plan (ambitious scope)

1.  Expand corpus (multiple frameworks), add **BM25+vector hybrid** in Weaviate; add **cross‑encoder re‑ranker** step.
2.  Replace router heuristic with a **bandit‑style router** (track success metrics per index).
3.  Add MCP tools: `drive.get` (evidence store), `pii.scan`, `ticket.create`, `controls.catalog`.
4.  **A2A**: introduce a _Risk Officer Agent_ for tie‑breaks; add negotiation states (`ACCEPT`, `DISPUTE`, `ESCALATE`).
5.  **Evals:** nDCG/MRR for retrieval; LLM‑as‑judge for mapping correctness; spot‑check human evals.
6.  **Observability:** structured events (OpenTelemetry), per‑edge timings, cost dashboards.
7.  **Multi‑tenant & permissions:** namespace isolation in vector stores; evidence scoping in tools.
8.  **Hardening:** prompt injections guard, PII redaction via MCP `pii.scan`, cached re‑usable reports.

**Full Roadmap (step‑by‑step)**

*   Data expansion → hybrid search & re‑rank → router learning → tool suite via MCP → 3‑agent negotiation loop → evaluation harness → telemetry → tenancy/ACL → red‑team and hardening → polished UI report.

### Resume wording (copy/adapt)

*   Built a **LangGraph‑orchestrated, multi‑agent Policy & Audit Copilot**; standardized tools with **MCP**; implemented **A2A** negotiation among _Auditor_, _Org Security_, _Risk Officer_ agents to resolve control evidence.
*   Delivered **vendor‑agnostic retrieval** with **Pinecone/Weaviate/FAISS** and a learning **retrieval router**, improving top‑3 accuracy by **X%** and reducing latency by **Y%**.
*   Applied **ICL/CoT** via structured reasoning (claims/evidence/gaps), hybrid search + re‑rank, and report assembly with guardrails (PII redaction, injection defenses).

* * *

Option 2 — **Incident Command Copilot**
---------------------------------------

_A system that monitors logs/metrics, hypothesizes root causes, locates relevant runbooks, and drafts remediation steps._

### Why interviewers will love it

*   Bridges **observability data** to LLMs with safe read‑only tools.
*   Shows **decision‑making under uncertainty** and agent debate (hypotheses ↔ evidence).
*   Great story for **latency budgets and fallbacks** across vector stores.

### Where each required tech shows up

*   **LangGraph:**  
    Nodes: _Signal Ingest_, _Planner_, _Hypothesis Generator_, _Runbook Retriever_, _Fix Suggester_, _Coordinator_.  
    State includes suspicion scores and confidence thresholds controlling edges.
*   **MCP:**  
    Tools for `metrics.query` (Prometheus/Grafana), `logs.search` (ELK), `kb.search` (runbooks), `deploy.read` (Kubernetes manifests, read‑only). All standardized under MCP.
*   **A2A:**  
    _Hypothesis Agent_ ↔ _Evidence Agent_ exchange: propose → test → revise. _Coordinator Agent_ arbitrates and drafts a status update.
*   **Vector DBs:**
    *   **Pinecone** — historic incident reports/runbooks at scale.
    *   **Weaviate** — config objects indexed with rich filters (service, cluster, region).
    *   **FAISS** — ephemeral cache of current incident chunks for ultra‑fast “near‑context” lookups.
*   **CoT/ICL:**  
    ICL templates for _fault trees_ and _post‑mortem outlines_. Structured scratchpad tracks “hypothesis → evidence → confidence”.
*   **Multi‑agent pipeline:**  
    Ingest → Hypothesis → Evidence retrieval → Remediation drafting → Executive summary.

### MVP Plan

**Goal:** Given a mock alert (e.g., 5xx spike), output “likely root causes + links to relevant runbooks.”

1.  Load a small synthetic logs/metrics dataset plus a few runbooks.
2.  Index runbooks in **Pinecone**; configs in **Weaviate**; incident snippets in **FAISS**.
3.  MCP servers: `logs.search`, `metrics.query`, `kb.search`.
4.  **LangGraph**: _Planner_ → _Hypothesis Agent_ → _Evidence Agent_ → _Fix Suggester_.
5.  Simple retrieval router; structured ICL for fault‑tree reasoning.
6.  CLI demo: alert in → hypotheses out → ranked runbooks + actions.

**MVP Roadmap**

*   Curate sample data → build indices (3 backends) → MCP tools → LangGraph skeleton → A2A loop (hypothesis/evidence) → output remediation draft.

### Complete Plan

1.  Live(ish) data adapters (record/replay traces), metadata‑aware filters in Weaviate, cross‑encoder re‑rank.
2.  Adaptive router with latency/cost/precision scores; FAISS hot cache invalidation.
3.  Additional MCP tools: `pager.notify` (mock), `k8s.read`, `feature_flags.read`.
4.  _Fix Suggester Agent_ checks safety policy (no direct writes) and drafts a change request as a ticket.
5.  Evaluation harness: measure hypothesis precision/recall, time‑to‑useful suggestion.
6.  Observability & cost tracking; executive dashboards.
7.  Incident replay & post‑mortem generator; risk scoring and playbook recommendations.

**Full Roadmap**

*   Adapters → hybrid retrieval → router learning → tool expansion → safety checks & ticketing → eval & telemetry → post‑mortems → dashboards.

### Resume wording

*   Created an **Incident Command Copilot** with **LangGraph** orchestrating hypothesis/evidence _A2A_ loops; standardized observability and knowledge tools via **MCP**.
*   Implemented **multi‑index retrieval** (Pinecone/Weaviate/FAISS) with an adaptive router, cutting “time‑to‑runbook” by **X%**; leveraged **ICL** fault‑tree templates and structured CoT for reliable remediation drafts.

* * *

Option 3 — **Account Research & Outreach Studio**
-------------------------------------------------

_A multi‑agent pipeline that researches a target company, synthesizes insights, drafts compliant outreach, and handles objections._

### Why interviewers will love it

*   Business‑facing impact; easy to demo end‑to‑end value.
*   Highlights **content personalization** with strong retrieval + **ICL style control**.
*   Demonstrates **A2A negotiation** (e.g., _Legal_ vs _Sales_ agents) and compliance.

### Where each required tech shows up

*   **LangGraph:**  
    Nodes: _Research Planner_, _Web/Doc Retriever_, _Insight Synthesizer_, _Persona Stylist_, _Objection Handler_, _QA Reviewer_.
*   **MCP:**  
    Tools for `web.fetch` (scraped cache or API), `crm.lookup`, `kb.search`, `safety.check` (brand/legal guardrails). Same schema, swappable implementations.
*   **A2A:**  
    _Sales Agent_ ↔ _Legal Agent_ review cycle over claims, compliance terms, and opt‑out language; _Pricing Agent_ provides constraints.
*   **Vector DBs:**
    *   **Pinecone** — large web profiles and historical notes.
    *   **Weaviate** — entity‑centric store (company, role, industry) with filters for targeting.
    *   **FAISS** — local cache for user‑specific snippets and recent calls.
*   **CoT/ICL:**  
    Style exemplars per persona; structured rationale fields (“insight → evidence → outreach line”).
*   **Multi‑agent pipeline:**  
    Research → Synthesis → Draft → Compliance → Finalize.

### MVP Plan

**Goal:** For a single company, produce a one‑pager with 5 insights and an outreach draft.

1.  Build a small cached corpus (company pages, blogs, reports).
2.  Index: Pinecone (long articles), Weaviate (entities/tags), FAISS (personal notes).
3.  MCP servers: `kb.search`, `crm.lookup`, `safety.check` (mock).
4.  **LangGraph**: _Research Planner_ → _Retriever_ → _Synthesizer_ → _Persona Stylist_ → _QA Reviewer_.
5.  Add ICL for tone and a structured insight schema.
6.  CLI demo outputs one‑pager + email draft.

**MVP Roadmap**

*   Corpus & indexing → MCP tools → LangGraph pipeline → persona ICL → QA check → deliver one‑pager and email.

### Complete Plan

1.  Multi‑account batch flow with dedup and cross‑account insight reuse; Weaviate hybrid search.
2.  Router with cost/latency budgets and source‑credibility scoring; cross‑encoder re‑rank.
3.  A2A: introduce _Objection Handler Agent_ and _Pricing Agent_; _Legal Agent_ signs off via contract templates.
4.  Add **feedback learning**: user edits inform ICL bank and retrieval routing weights.
5.  Evals: personalization score (LLM‑judge), factuality checks, response‑rate A/B framework (simulated or small trials).
6.  Safety: reference tracking for every claim; automatic link‑back “citations” section.

**Full Roadmap**

*   Batch processing → improved retrieval → agent expansions & negotiations → feedback learning → evals & safety → reporting.

### Resume wording

*   Built a **multi‑agent Account Research Studio** orchestrated with **LangGraph**; standardized CRM/web/kb access via **MCP**; implemented **A2A** compliance reviews between Sales/Legal/Pricing agents.
*   Delivered **personalized outreach** with a vendor‑agnostic retrieval layer (**Pinecone/Weaviate/FAISS**) and **ICL** style controls, improving insight relevance by **X%** and draft acceptance by **Y%**.

* * *

Option 4 — **Literature Navigator & Reviewer**
----------------------------------------------

_A research assistant that ingests PDFs, builds a claim‑evidence graph, compares papers, and drafts a mini‑review._

### Why interviewers will love it

*   Academic rigor story: **claims vs. evidence** with citation tracking.
*   Shows **graph‑aware retrieval** (Weaviate metadata, FAISS cache, Pinecone scale).
*   Clean **A2A debate** (Reader ↔ Critic ↔ Synthesizer).

### Where each required tech shows up

*   **LangGraph:**  
    Nodes: _PDF Ingestor_, _Claim Extractor_, _Evidence Finder_, _Critic_, _Synthesizer_, _Reference Verifier_.
*   **MCP:**  
    Tools for `pdf.parse`, `papers.search` (catalog API), `citations.resolve`, `kb.search`.
*   **A2A:**  
    _Reader Agent_ proposes claims; _Critic Agent_ challenges and seeks counter‑evidence; _Synthesizer Agent_ reconciles and drafts sections.
*   **Vector DBs:**
    *   **Pinecone** — embeddings for long PDF chunks across many papers.
    *   **Weaviate** — metadata filters (venue, year, keywords) and cross‑refs for related work.
    *   **FAISS** — fast local cache for the active reading session.
*   **CoT/ICL:**  
    ICL exemplars for “claim‑evidence‑limitation” triples; structured review outline; no raw free‑form CoT leakage.
*   **Multi‑agent pipeline:**  
    Ingestion → Extraction → Cross‑paper comparison → Draft review → Reference verification.

### MVP Plan

**Goal:** Given 5 PDFs, output a 2‑page structured mini‑review with claims and citations.

1.  Parse PDFs; chunk text/figures.
2.  Index chunks across **Pinecone**, **Weaviate** (with metadata), and **FAISS** (session cache).
3.  MCP servers: `pdf.parse`, `kb.search`, `citations.resolve`.
4.  **LangGraph** agents: _Claim Extractor_ → _Evidence Finder_ → _Critic_ → _Synthesizer_.
5.  ICL templates for claim/evidence/limitations; output with inline references.

**MVP Roadmap**

*   PDF parsing → tri‑index build → MCP tools → agent chain → review draft.

### Complete Plan

1.  Add table/figure extraction and caption‑aware retrieval; cross‑encoder re‑rank.
2.  _Verifier Agent_ checks reference integrity; _Contradiction Agent_ hunts for conflicts.
3.  Router learns to prefer Weaviate when filters are present; Pinecone for breadth; FAISS for iterative reading loops.
4.  Evals: factuality (citation coverage), novelty score, coverage metrics per section.
5.  Export to markdown/LaTeX and auto‑generated “related work” graph.

**Full Roadmap**

*   Advanced extraction → verification agents → router learning → evals → publishing pipeline.

### Resume wording

*   Delivered a **Literature Navigator** using **LangGraph** multi‑agent debate (Reader/Critic/Synthesizer) with **MCP** tools for PDF parsing and citation resolution; deployed **Pinecone/Weaviate/FAISS** retrieval with a learning router and **ICL** claim‑evidence templates to draft verifiable mini‑reviews.

* * *

Cross‑cutting guidance (applies to all options)
-----------------------------------------------

**Retrieval Router (core interview topic)**

*   Start rule‑based (filters → Weaviate; large/general → Pinecone; session/fast‑rerank → FAISS).
*   Log outcomes (clicks, judge scores), then upgrade to a lightweight bandit or score‑based policy.
*   Show de‑duplication and source diversity (MMR) across backends.

**Reasoning Patterns without leaking raw CoT**

*   Use **structured scratchpads** (e.g., JSON for “hypothesis, evidence, decision, confidence”) instead of free‑form chain‑of‑thought.
*   Keep a curated **ICL bank** (few high‑quality exemplars per task).
*   Add a **self‑check** node that verifies outputs against retrieved facts.

**Evaluation you can explain concisely**

*   Retrieval: nDCG@k, MRR, recall@k; qualitative spot‑checks.
*   Generation: LLM‑judge with simple rubrics (factuality, relevance, actionability), plus human review on small samples.
*   System: latency, cost per task, success rate; traces per edge (OpenTelemetry).

**Security & safety talking points**

*   MCP tool scopes (read‑only by default); input/output redaction; prompt‑injection defenses; per‑tenant namespaces in vector stores.

**Demo script for interviews**

1.  Show the **LangGraph** diagram.
2.  Run a **single query end‑to‑end** (MVP).
3.  Open the **router log** comparing Pinecone vs. Weaviate vs. FAISS decisions.
4.  Show the **agent debate transcript** (high‑level messages, not raw CoT).
5.  Display the **final artifact** (audit packet, incident summary, one‑pager, or mini‑review).

* * *

Picking one & next steps
------------------------

If you need a short path to credibility, Option 1 or Option 2 tends to land best with infra/AI teams; Option 3 resonates with GTM‑oriented orgs; Option 4 fits research‑heavy roles. Start with the MVP steps, then iterate toward the Complete Plan by adding the router, the third vector backend, and A2A negotiation.

## Prompt:
You are a senior AI platform and retrieval systems architect. Please produce a complete, executable MVP project plan document (text only, no code) for building an “Account Research & Outreach Studio”. The goal is to cover data preparation → indexing → retrieval routing → multi-agent collaboration → compliance template → evaluation → deliverables.
Constraints (must follow)
You must choose one suitable public company yourself (preferably a tech company with abundant public filings and website materials). Explain why you chose it.
MVP scope only: Input = “company + persona”; Output = one-page insights (5 insights, each with source/date) + one outreach email draft (with unsubscribe line + company info). Do not write any code.
You must find and list concrete data sources with direct links (e.g., SEC 10-K/10-Q/8-K, company website press/blog, Wikipedia).
You must explicitly cover and anchor:
LangGraph nodes & state flow
MCP tool contracts
A2A roles & message schema
Multi-vector DB usage (Pinecone / Weaviate / FAISS) and retrieval routing
ICL / structured reasoning
Evaluation (retrieval, generation, compliance)
Output should be a step-by-step execution plan, not general advice.
Every part must be quantifiable (thresholds, scoring dimensions, pass criteria).
Provide a 5-day timeline with milestones and a list of deliverables.
Key Requirements
Produce a data inventory table: for each source list URL, purpose, time coverage, priority, and metadata fields (doctype, date, section, topic, source, url, title, company, persona_tags).
In system design, define LangGraph nodes with inputs/outputs and transition rules.
In tools, define MCP tool contracts (params, return, error handling).
In agents, define at least two roles (Sales vs Legal/Brand) and a message schema.
In retrieval, explain roles of Pinecone, Weaviate, FAISS and provide routing heuristics + logging fields.
In reasoning, define a schema for “insight cards” and for the email draft (fields only, not actual text).
In evaluation, specify metrics and thresholds for retrieval, generation, and compliance.
In timeline, provide clear daily deliverables (≤ 5 days).
In deliverables, list all required artifacts (docs, schemas, templates, sample evaluations).
In risks, analyze data availability, site rate limits, citation consistency, and give mitigations.
In extensions, list possible future features (cross-encoder rerank, routing learning, multi-company, persona expansion).

“””
I choose Option 3 — Account Research & Outreach Studio
A multi‑agent pipeline that researches a target company, synthesizes insights, drafts compliant outreach, and handles objections.
Why interviewers will love it
Business‑facing impact; easy to demo end‑to‑end value.
Highlights content personalization with strong retrieval + ICL style control.
Demonstrates A2A negotiation (e.g., Legal vs Sales agents) and compliance.
Where each required tech shows up
LangGraph:
Nodes: Research Planner, Web/Doc Retriever, Insight Synthesizer, Persona Stylist, Objection Handler, QA Reviewer.
MCP:
Tools for web.fetch (scraped cache or API), crm.lookup, kb.search, safety.check (brand/legal guardrails). Same schema, swappable implementations.
A2A:
Sales Agent ↔ Legal Agent review cycle over claims, compliance terms, and opt‑out language; Pricing Agentprovides constraints.
Vector DBs:
Pinecone — large web profiles and historical notes.
Weaviate — entity‑centric store (company, role, industry) with filters for targeting.
FAISS — local cache for user‑specific snippets and recent calls.
CoT/ICL:
Style exemplars per persona; structured rationale fields (“insight → evidence → outreach line”).
Multi‑agent pipeline:
Research → Synthesis → Draft → Compliance → Finalize.
MVP Plan
Goal: For a single company, produce a one‑pager with 5 insights and an outreach draft.
Build a small cached corpus (company pages, blogs, reports).
Index: Pinecone (long articles), Weaviate (entities/tags), FAISS (personal notes).
MCP servers: kb.search, crm.lookup, safety.check (mock).
LangGraph: Research Planner → Retriever → Synthesizer → Persona Stylist → QA Reviewer.
Add ICL for tone and a structured insight schema.
CLI demo outputs one‑pager + email draft.
MVP Roadmap
Corpus & indexing → MCP tools → LangGraph pipeline → persona ICL → QA check → deliver one‑pager and email.
Complete Plan
Multi‑account batch flow with dedup and cross‑account insight reuse; Weaviate hybrid search.
Router with cost/latency budgets and source‑credibility scoring; cross‑encoder re‑rank.
A2A: introduce Objection Handler Agent and Pricing Agent; Legal Agent signs off via contract templates.
Add feedback learning: user edits inform ICL bank and retrieval routing weights.
Evals: personalization score (LLM‑judge), factuality checks, response‑rate A/B framework (simulated or small trials).
Safety: reference tracking for every claim; automatic link‑back “citations” section.
Full Roadmap
Batch processing → improved retrieval → agent expansions & negotiations → feedback learning → evals & safety → reporting.

“””

## Response:
Request for GPT-5 Pro

Reasoned for 12m 44s

Below is a **complete, executable MVP project plan (text only, no code)** for building the **Account Research & Outreach Studio**.

* * *

0) Target Company & Rationale
-----------------------------

**Chosen company:** **Salesforce, Inc. (NYSE: CRM)**  
**Why:** Salesforce provides abundant, current, and structured public materials (SEC filings, earnings press releases, product pages, newsroom/blog), which makes it ideal for a retrieval‑first MVP focused on B2B outreach. Examples include the FY25 Form 10‑K, quarterly filings, 8‑Ks, an active investor news site, and a high‑volume newsroom/blog. [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)[Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?utm_source=chatgpt.com)[Salesforce+1](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)[Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)

**MVP input → output**

*   **Input:** `"company + persona"`, e.g., `"Salesforce" + "VP of Customer Experience"`.
*   **Output:**
    1.  **One‑page insights** containing **exactly 5 insights**, each with **source URL + publication date**; insights must be **persona‑relevant**.
    2.  **One outreach email draft** with **unsubscribe line** and **company info block**.

**Success criteria (MVP):**

*   5 insights produced with **≥1 distinct source each**; at least **4 distinct sources overall**; at least **2 insights** from items **≤ 12 months old**.
*   Email draft includes **subject**, **personalization**, **CTA**, **unsubscribe**, **company info block**.
*   **Factuality**: 100% of claims cite a source; **broken links = 0**.
*   **Latency (median)**: ≤ **30s** end‑to‑end; **retrieval** ≤ **2.5s** per query.
*   **Compliance pass rate** (template checks): **100%** critical checks.
*   **Evaluation thresholds** (details in §9): Retrieval **Recall@10 ≥ 0.80**, nDCG@5 **≥ 0.60** on seed set; Generation LLM‑judge **≥ 4.0/5** on relevance & specificity; Compliance: **all critical checks green**.

* * *

1) Data Inventory (Concrete Sources)
------------------------------------

**Company:** Salesforce, Inc.

| Source name | URL | Purpose | Time coverage | Priority (1=highest) | Metadata fields captured (per document) |
| --- | --- | --- | --- | --- | --- |
| SEC Company filings (landing) | [https://www.sec.gov/edgar/browse/?CIK=0001108524](https://www.sec.gov/edgar/browse/?CIK=0001108524) | Canonical filings index (10‑K/10‑Q/8‑K) | 2004–present | 1 | doctype, date, section, topic, source, url, title, company, persona\_tags [SEC](https://www.sec.gov/edgar/browse/?CIK=0001108524&utm_source=chatgpt.com) |
| FY25 Form 10‑K (HTML) | [https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm) | Risk factors, strategy, segments, financials | FY25 (filed Mar 2025) | 1 | doctype=10‑K, date, section, topic, source, url, title, company, persona\_tags [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com) |
| FY26 Q1 10‑Q (HTML) | [https://www.sec.gov/Archives/edgar/data/1108524/000110852425000030/crm-20250430.htm](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000030/crm-20250430.htm) | Recent quarterly updates | Q filed Jun 2025 | 1 | doctype=10‑Q, date, section, topic, source, url, title, company, persona\_tags [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000030/crm-20250430.htm?utm_source=chatgpt.com) |
| 8‑K earnings release (Feb 26, 2025) | [https://www.sec.gov/ix?doc=/Archives/edgar/data/1108524/000110852425000002/crm-20250226.htm](https://www.sec.gov/ix?doc=/Archives/edgar/data/1108524/000110852425000002/crm-20250226.htm) | Official earnings press as exhibit | Feb 2025 | 1 | doctype=8‑K, date, section, topic, source, url, title, company, persona\_tags [SEC](https://www.sec.gov/ix?doc=%2FArchives%2Fedgar%2Fdata%2F1108524%2F000110852425000002%2Fcrm-20250226.htm&utm_source=chatgpt.com) |
| Investor News (press releases) | [https://investor.salesforce.com/news/default.aspx](https://investor.salesforce.com/news/default.aspx?utm_source=chatgpt.com) | Financial PR & transaction updates | Rolling 12–24 months | 2 | doctype=press, date, topic, source, url, title, company, persona\_tags [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?utm_source=chatgpt.com) |
| Salesforce Newsroom (all news & press) | [https://www.salesforce.com/news/all-news-press-salesforce/](https://www.salesforce.com/news/all-news-press-salesforce/) | Product/customer stories & announcements | Rolling 12–24 months | 2 | doctype=press/blog, date, topic, source, url, title, company, persona\_tags [Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com) |
| Press Releases (filterable) | [https://www.salesforce.com/news/content-types/press-releases/](https://www.salesforce.com/news/content-types/press-releases/?utm_source=chatgpt.com) | General corporate/product news | Rolling 12–24 months | 3 | doctype=press, date, topic, source, url, title, company, persona\_tags [Salesforce](https://www.salesforce.com/news/content-types/press-releases/?utm_source=chatgpt.com) |
| Official Blog (The 360 Blog) | [https://www.salesforce.com/blog/](https://www.salesforce.com/blog/?utm_source=chatgpt.com) | Thought leadership & product tips | Rolling | 3 | doctype=blog, date, topic, source, url, title, company, persona\_tags [Salesforce](https://www.salesforce.com/blog/?utm_source=chatgpt.com) |
| Product page: Agentforce | [https://www.salesforce.com/agentforce/](https://www.salesforce.com/agentforce/) | Product positioning & use cases | Current | 2 | doctype=product, date (scrape), topic, source, url, title, company, persona\_tags [Salesforce](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com) |
| Product page: Data Cloud | [https://www.salesforce.com/data/](https://www.salesforce.com/data/) | Data strategy, platform claims | Current | 2 | doctype=product, date (scrape), topic, source, url, title, company, persona\_tags [Salesforce](https://www.salesforce.com/data/?utm_source=chatgpt.com) |
| Developer Guide: Agent API | [https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html) | Technical capabilities | Current | 3 | doctype=docs, date, topic, source, url, title, company, persona\_tags [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com) |
| Help Docs: Data Cloud | https://help.salesforce.com/s/articleView?id=data.c360\_a\_data\_cloud.htm&type=5 | Capabilities & terminology | Current | 3 | doctype=docs, date, topic, source, url, title, company, persona\_tags [Salesforce](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud.htm&language=en_US&type=5&utm_source=chatgpt.com) |
| Wikipedia | [https://en.wikipedia.org/wiki/Salesforce](https://en.wikipedia.org/wiki/Salesforce) | General background | Current | 4 | doctype=wiki, date (scrape), topic, source, url, title, company, persona\_tags [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com) |

**Notes:**

*   For 10‑K PDF alternate: FY25 Annual Report PDF (visual) if needed for quoting charts: [https://www.sec.gov/Archives/edgar/data/1108524/000110852425000019/salesforce\_fy25annualreport.pdf](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000019/salesforce_fy25annualreport.pdf). [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000019/salesforce_fy25annualreport.pdf?utm_source=chatgpt.com)

* * *

2) Data Preparation (MVP)
-------------------------

**Objective:** produce normalized, deduplicated, chunked text with consistent metadata for indexing.

**Steps & thresholds**

1.  **Discovery & fetch:** Pull only pages within the inventory above; depth=1 for newsroom/blog. **Max pages:** 120. **Robots & rate‑limit:** ≤ 6 requests/sec, backoff 2× on 429.
2.  **Normalization:**
    *   Strip boilerplate, nav, cookie banners.
    *   Extract **title**, **publish date** (prefer structured date; else infer from page/filing header), **doctype**, **section** (e.g., “Risk Factors”), **topic** tags from headings or press categories, **source**, **url**, **company**, **persona\_tags** (keyword mapping).
    *   **Date coverage requirement:** ≥ 30 items within last 24 months.
3.  **Chunking:** semantic sections or sliding window **800 tokens** with **120 token overlap**; per chunk attach metadata above.
4.  **Deduping:** MinHash or URL canonicalization + content hash; drop near‑duplicates with Jaccard ≥ 0.85.
5.  **Quality gates:**
    *   **Missing date** ≤ 5% of docs (else flag).
    *   **Broken link rate** (on resolve) = 0.
    *   **Non‑English** < 5% (drop or tag).

* * *

3) Indexing (Multi‑Vector)
--------------------------

**Goal:** maintain three complementary indices and a simple re‑rank cache.

*   **Pinecone (managed, scale):**
    *   **Role:** long‑form breadth (10‑K, 10‑Q, newsroom features).
    *   **Namespace:** `crm_longform_v1`.
    *   **Metadata fields:** doctype, date, section, topic, url, title, company, persona\_tags, source\_domain.
    *   **Top‑k default:** 12.
*   **Weaviate (metadata & hybrid):**
    *   **Role:** entity/field‑aware retrieval and **keyword+vector hybrid** (for “filter: topic=Agentforce, doctype=press, date>=2025‑01‑01”).
    *   **Class schema:** `Doc{ text, vector, doctype, date, section, topic, url, title, company, persona_tags, source_domain }`.
    *   **Top‑k default:** 12.
*   **FAISS (local/session cache):**
    *   **Role:** fast **session‑level** cache of **the last 300 chunks** (from Pinecone/Weaviate results + any user notes) for iterative summarization and cross‑evidence checks.
    *   **Top‑k default:** 25; used for **re‑rank** and **diversity**.

**Index build acceptance:**

*   **Index load success:** 100% of items; any rejects logged with reason.
*   **Embedding coverage:** 100% of chunks.
*   **Metadata completeness:** required fields present in **≥ 98%** of chunks.

* * *

4) Retrieval Routing (MVP Heuristics + Logging)
-----------------------------------------------

**Router inputs:** query\_text, needed\_filters (e.g., `doctype=10-K`, `after=2025-01-01`), persona, recency\_bias (0–1), max\_latency\_ms.

**Decision rules (first match wins):**

1.  **Filter present** (doctype/topic/date/company/persona\_tags) → **Weaviate** (hybrid on).
2.  Query contains **“risk”, “RPO”, “operating margin”, “segment”, “competition”** → **Pinecone** (10‑K/10‑Q focus).
3.  Persona asks for **customer stories or PR** → **Weaviate** with `doctype in {press, blog}`.
4.  **Follow‑up/iterative** turn or synthesis stage → **FAISS** first; if **top\_k < 5 unique sources**, fall back to **Pinecone**.

**Post‑retrieval re‑rank:**

*   Merge results; compute **source diversity** and **date recency** score; take top 10 by **0.6·similarity + 0.3·recency + 0.1·diversity**; cache in **FAISS**.

**Router logging (persist every call):**

*   `route_id`, `timestamp`, `query_text`, `persona`, `decision_backend`, `reason_codes` (e.g., FILTER\_MATCH, PR\_QUERY, FOLLOWUP), `latency_ms`, `top_k`, `n_unique_domains`, `recency_avg_days`, `empty_result_flag`.

**Router acceptance:**

*   **Latency per call ≤ 700 ms** (Weaviate/FAISS) or **≤ 1500 ms** (Pinecone).
*   **Empty result rate ≤ 2%** (else auto‑retry alternate backend).

* * *

5) LangGraph Orchestration (Nodes, I/O, Transitions)
----------------------------------------------------

**Shared state (available to all nodes):**  
`company, persona, queries[], retrieved_chunks[], retrieval_logs[], insight_candidates[], insight_cards[], email_draft, compliance_flags[], metrics, route_decisions[], errors[]`

**Nodes:**

1.  **Intake & Normalize**
    *   **Input:** raw `company`, `persona`.
*   **Output:** `company_normalized`, `persona_profile` (keywords/ICL keys).
*   **Transition:** always → Research Planner.
    2.  **Research Planner**
    *   **Input:** `company_normalized`, `persona_profile`.
*   **Output:** `queries[]` (5–8 focused queries; e.g., “latest product launches”, “strategy & risks”, “financial highlights”, “customer stories in industry X”).
*   **Rule:** if fewer than **5 queries**, add from persona template. → Web/Doc Retriever.
    3.  **Web/Doc Retriever**
    *   **Input:** `queries[]`.
*   **Action:** call MCP `kb.search` per query; rely on router.
*   **Output:** `retrieved_chunks[]` (≥ 30); `retrieval_logs[]`.
*   **Retries:** if results < 20, expand queries with synonyms. → Insight Synthesizer.
    4.  **Insight Synthesizer**
    *   **Input:** `retrieved_chunks[]`.
*   **Output:** `insight_candidates[]` (8–10) with fields per schema (see §7).
*   **Rule:** ensure **source/date** present; drop any without date. → Evidence Consolidator.
    5.  **Evidence Consolidator**
    *   **Input:** `insight_candidates[]`.
*   **Action:** dedupe/merge similar; keep **top 5** by **persona\_relevance × recency × confidence**.
*   **Output:** `insight_cards[5]`. → Persona Stylist.
    6.  **Persona Stylist**
    *   **Input:** `insight_cards[5]`, `persona_profile`, ICL keys.
*   **Output:** stylized card texts (still structured; not free CoT) & seed lines for outreach. → A2A Review.
    7.  **A2A Review (Sales vs Legal/Brand)**
    *   **Input:** stylized cards & seed email fields.
*   **Action:** run **Sales Agent** proposal; **Legal/Brand Agent** checks compliance template; exchange up to **2 rounds**.
*   **Output:** `compliance_flags[]` (must be empty to proceed), finalized `insight_cards[5]` and structured `email_draft`.
*   **Transition:** if flags exist → Persona Stylist (one fix round); else → Final Assembler.
    8.  **Final Assembler**
    *   **Input:** `insight_cards[5]`, `email_draft`.
*   **Output:** final **one‑pager** and **email draft** objects (schemas §7).
*   **Done.**

**Graph exit conditions:**

*   Must have exactly **5** insight cards; if fewer, loop Insight Synthesizer → Retriever with fallback queries until 5 achieved or **max 2 loops** (then fail with error state).

* * *

6) MCP Tools (MVP Contracts)
----------------------------

> **All tools follow MCP: request → response with `status`, `data`, `error` (nullable), `metrics` (latency\_ms, backend). Timeouts: 8s.**

1.  **`kb.search`**
    *   **Params:**
    *   `query` (string), `filters` (key/val map; supports doctype/topic/date ranges), `top_k` (int≤20), `backend` (enum: pinecone|weaviate|faiss|auto), `recency_bias` (0–1).
*   **Returns (`data`)**: list of items with `doc_id`, `snippet`, `score` (0–1), `url`, `title`, `doctype`, `date`, `topic`, `section`, `company`, `persona_tags`, `source_domain`.
*   **Errors:** `RateLimited`, `BackendUnavailable`, `NoResults`.
*   **Behavior:** on `auto`, apply router rules in §4.
    2.  **`web.fetch`** (read‑only, cached)
    *   **Params:** `url`, `type_hint` (html|pdf), `max_bytes` (≤ 2MB).
*   **Returns:** `title`, `text`, `publish_date`, `status_code`, `canonical_url`.
*   **Errors:** `HTTPError`, `ParseError`, `TooLarge`.
    3.  **`crm.lookup`** (mock persona context)
    *   **Params:** `persona` (string).
*   **Returns:** `persona_profile` with `goals[]`, `pain_points[]`, `preferred_tone`, `kpis[]`, `topics[]`, `forbidden_claims[]`.
*   **Errors:** `PersonaUnknown`.
    4.  **`safety.check`** (mock brand/legal)
    *   **Params:** `email_fields` (subject, body\_sections\[\], links\[\], unsubscribe\_block, company\_info\_block).
*   **Returns:** `flags[]` (each: `code`, `severity`, `message`, `location`), e.g., `MISSING_UNSUBSCRIBE`, `UNCITED_CLAIM`, `PROHIBITED_PHRASE`.
*   **Errors:** `SchemaError`.
    5.  **`link.resolve`** (optional)
    *   **Params:** `url`.
*   **Returns:** `status_code`, `final_url`, `last_modified`.
*   **Errors:** `HTTPError`, `Timeout`.

* * *

7) Structured Reasoning & Output Schemas (no code, fields only)
---------------------------------------------------------------

**Insight Card (structured object)**

*   `id` (string)
*   `persona_relevance_score` (0–1)
*   `claim_summary` (≤ 35 words)
*   `evidence_snippets[]` (up to 2 snippets, each ≤ 30 words, quoted)
*   `source` (title)
*   `url` (canonical)
*   `doctype` (10‑K|10‑Q|8‑K|press|blog|product|docs|wiki)
*   `publish_date` (ISO‑8601)
*   `business_impact` (enum: revenue|cost|risk|customer\_experience|strategy)
*   `confidence` (0–1, derived from retrieval score & source credibility)
*   `notes_for_outreach` (1–2 lines keyed to persona KPIs)

**Outreach Email Draft (structured object)**

*   `subject`
*   `greeting` (uses persona name placeholder)
*   `personalization_fields` (company, persona, referenced\_insight\_ids\[2–3\])
*   `value_proposition` (1–2 lines, tied to insights)
*   `proof_points[]` (2–3 short bullets referencing insights by id)
*   `call_to_action` (one CTA)
*   `optional_P.S.`
*   `unsubscribe_block` (explicit opt‑out sentence + link placeholder)
*   `company_info_block` (legal name, street address, city, state, zip, website)

**ICL/Prompting assets (non‑CoT leakage):**

*   **Persona exemplars:** 3 mini‑records per persona (tone, do/don’t, KPI keywords).
*   **Insight examples:** 5 example insight cards (structure only, not claims).
*   **Email skeleton:** subject styles, CTA phrasing templates per persona.

* * *

8) Agents (A2A)
---------------

**Roles:**

*   **Sales Agent (Proposer):** maximizes persona relevance & clarity; composes email structure using insight ids.
*   **Legal/Brand Agent (Reviewer):** enforces compliance, citation presence, factuality from allowed sources, and brand bans.

**Message schema (each exchange)**

*   `role` (sales|legal\_brand)
*   `type` (PROPOSAL|CRITIQUE|REVISION|APPROVAL)
*   `payload_ref` (insight\_card\_ids\[\], email\_field\_names\[\])
*   `comments[]` (each with `location`, `requirement`, `severity`)
*   `decision` (PENDING|CHANGES\_REQUIRED|APPROVED)

**A2A loop rules**

*   Start with **Sales PROPOSAL**; **Legal/Brand CRITIQUE** within 1 pass; **Sales REVISION**; **Legal/Brand APPROVAL**.
*   **Max 2 rounds**; if still failing, escalate with error state containing blocking flags.
*   **Approval gates:** `MISSING_UNSUBSCRIBE`\=none, `UNCITED_CLAIM`\=none, forbidden phrases=none.

* * *

9) Evaluation Plan (MVP)
------------------------

**Gold set:** 10 prompts (company + persona), covering at least **3 personas**.

**Retrieval metrics (per prompt):**

*   **Recall@10** (did we retrieve at least one correct doc for each insight?) **≥ 0.80**.
*   **nDCG@5** **≥ 0.60**.
*   **Coverage:** ≥ **4 unique sources** in candidate pool.
*   **Freshness:** mean document age ≤ **540 days**.
*   **Link health:** 100% HTTP 200 via `link.resolve`.

**Generation metrics (LLM‑judge rubric 1–5):**

*   **Persona relevance ≥ 4.0**, **Specificity ≥ 4.0**, **Actionability ≥ 4.0**, **Fluff ≤ 2.0**.
*   **Citations alignment:** every claim maps to a retrieved source (binary). **Target: 100%**.

**Compliance metrics:**

*   **Critical checks:** unsubscribe present, company info present, no prohibited claims → **100% pass**.
*   **Style checks:** reading grade ≤ 10 (Flesch‑Kincaid approximation); email length ≤ 160 words body (±10%).
*   **Diversity:** insights use ≥ **2** SEC items or ≥ **1** SEC + ≥ **2** press/blog items.

**Pass/Fail (MVP sign‑off):** must meet **all** compliance targets and **≥ 80%** of retrieval+generation thresholds.

* * *

10) Compliance Template (MVP)
-----------------------------

**Legal/Brand checklist (binary unless noted):**

*   Unsubscribe sentence with link placeholder **present**.
*   Company info block **present** (legal name & postal address).
*   All **claims** reference **allowed sources** (SEC filings, official press/blog, product/help pages, or Wikipedia for background; third‑party media optional).
*   No **superlatives** without source (“#1 AI CRM” allowed only if cited from official pages). [Salesforce Investor Relations](https://investor.salesforce.com/news/news-details/2025/Salesforce-Announces-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx?utm_source=chatgpt.com)
*   No competitive disparagement.
*   **PII:** none.
*   **Trademarks:** ™/® only if present in source.
*   Reading grade ≤ 10; body ≤ 160 words; single CTA.

* * *

11) Step‑by‑Step Execution Plan (MVP)
-------------------------------------

**Phase A — Data & Indexes**

1.  Build the **data inventory** from §1.
2.  Run **fetch/normalize** for all listed URLs (cap 120 pages).
3.  Create chunked corpus with required metadata (quality gates in §2).
4.  Index to **Pinecone**, **Weaviate**, **FAISS** (schemas in §3).
5.  Validate index health (completeness ≥ 98%, broken links=0).

**Phase B — Tools & Router**  
6\. Implement MCP tools (`kb.search`, `web.fetch`, `crm.lookup`, `safety.check`, `link.resolve`).  
7\. Implement **router** with rules in §4 and **logging**; verify latency budgets per backend.  
8\. Dry‑run test: 5 sample queries; inspect logs for diversity/recency.

**Phase C — LangGraph & Agents**  
9\. Wire **LangGraph** nodes & state as in §5 (happy path first).  
10\. Add **Sales** and **Legal/Brand** agents with the **message schema** in §8; allow 2 rounds.  
11\. Insert **ICL assets** (persona exemplars, insight skeletons, email skeleton).

**Phase D — Evaluation & Hardening**  
12\. Build a **seed gold set** (10 prompts; 3 personas).  
13\. Run **retrieval metrics** (Recall@10, nDCG@5, freshness, link health).  
14\. Generate **one‑pagers + emails** for 5 prompts; score with LLM‑judge and compliance tool.  
15\. Remediate gaps (router tweaks, persona keywords), re‑run until thresholds met.

**Phase E — Packaging**  
16\. Produce **final artifacts** (schemas, logs, example outputs) and a short **demo script**.

* * *

12) 5‑Day Timeline & Milestones
-------------------------------

**Day 1 — Data & Schema**

*   Inventory finalized; fetch 120 pages max; normalization + chunking complete; metadata dictionary frozen.
*   **Milestones:** ≥ 80 docs with dates; dedupe done; link health 100%.
*   **Deliverables:** Data inventory CSV, metadata dictionary, normalization rules.

**Day 2 — Indexes & Tools**

*   Pinecone/Weaviate/FAISS built; MCP `kb.search`, `web.fetch`, `link.resolve` online; router v1 logging.
*   **Milestones:** index completeness ≥ 98%; router latency within budget.
*   **Deliverables:** Index specs, router heuristics doc, tool contracts.

**Day 3 — Graph & Agents**

*   LangGraph nodes wired; A2A loop (Sales ↔ Legal/Brand) functional; ICL assets installed.
*   **Milestones:** end‑to‑end happy path produces 5 insights + email draft.
*   **Deliverables:** Graph state spec, agent message schema, compliance template.

**Day 4 — Evaluation & Tuning**

*   Seed gold set (10 prompts); run retrieval & generation evals; fix routing and persona mappings.
*   **Milestones:** Retrieval thresholds met; generation LLM‑judge ≥ 4.0/5 avg; compliance 100%.
*   **Deliverables:** Eval report v1, router log samples, example outputs (3 sets).

**Day 5 — Finalization**

*   Documentation, risk review, and packaging; demo script.
*   **Milestones:** MVP sign‑off (all success criteria met).
*   **Deliverables:** Final one‑pager+email sample for “Salesforce + VP of Customer Experience”, full artifact pack.

* * *

13) Final Deliverables (MVP)
----------------------------

1.  **Data inventory** (table/CSV) with URLs and metadata coverage stats.
2.  **Metadata dictionary** (field definitions & fill rules).
3.  **Index specifications** (per backend) and index health report.
4.  **MCP tool contracts** (params/returns/errors) and ping tests.
5.  **Router heuristics** & **sample decision logs**.
6.  **LangGraph spec** (nodes, I/O, transitions) and state diagram (text description acceptable).
7.  **Agent message schema**, **ICL assets list**, **compliance template**.
8.  **Evaluation report** (retrieval metrics, generation scores, compliance results).
9.  **Example outputs**: one‑pager (5 insight cards) + email draft objects for at least **3 personas**.
10.  **Risk register** with mitigations.
11.  **Demo script** (runbook for acceptance).

* * *

14) Risks & Mitigations
-----------------------

*   **Data availability / volatility:** newsroom URLs and filing links can change; use SEC canonical links and newsroom category feeds; run `link.resolve` nightly; keep **recrawl cadence weekly**. [SEC](https://www.sec.gov/edgar/browse/?CIK=0001108524&utm_source=chatgpt.com)[Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
*   **Rate limits:** SEC and site throttling; cap to **≤ 6 rps**, exponential backoff, local cache of fetched HTML/PDF.
*   **Citation consistency:** enforce **source/date required** at Insight Synthesizer; `UNCITED_CLAIM` flagged by `safety.check` blocks release.
*   **Over‑fitting to one backend:** log **backend success rate** and rotate fallbacks; ensure **empty‑result auto‑retry** on alternate store.
*   **Stale insights:** freshness floor in router (prefer items ≤ 18 months; require ≥ 2 ≤ 12 months).
*   **Persona mismatch:** require **persona\_relevance\_score ≥ 0.7** for all 5 insights; else regenerate with persona‑specific queries.

* * *

15) Extensions (post‑MVP)
-------------------------

*   **Cross‑encoder re‑ranker** for semantic precision.
*   **Learning router** (bandit) using success metrics (clicked/cited).
*   **Multi‑company batch mode** and caching of cross‑account insights.
*   **Persona expansion** with dynamic tone/style selection and per‑industry KPIs.
*   **Confidence calibration** using source credibility weights (SEC > investor PR > newsroom > wiki).
*   **Automatic citation snippets** with span highlighting.
*   **A/B testing harness** for subject lines & CTAs.
*   **More agents** (Pricing, Objection Handler) with measurable negotiation outcomes.

* * *

16) Example Source Anchors (for your corpus)
--------------------------------------------

*   **SEC filings (canonical):** FY25 10‑K; FY26 Q1 10‑Q; Feb 2025 8‑K. [SEC+2SEC+2](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
*   **Investor news & newsroom:** investor releases and all‑news page. [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?utm_source=chatgpt.com)[Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
*   **Product references:** Agentforce & Data Cloud product pages and docs. [Salesforce+1](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com)[Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)[Salesforce](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud.htm&language=en_US&type=5&utm_source=chatgpt.com)
*   **Background:** Wikipedia overview page. [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)

* * *

### What interviewers see in this MVP

*   **LangGraph**: clear, auditable orchestration with deterministic transitions.
*   **MCP**: standardized tools that make sources swappable.
*   **A2A**: measurable Sales↔Legal negotiation with pass/fail gates.
*   **Multi‑vector retrieval**: practical backend routing with logs and thresholds.
*   **ICL & structured reasoning**: insight cards & email schema enforce traceability.
*   **Evaluations**: concrete metrics with pass criteria tied to business‑ready outputs.

This plan gives you a **tight, five‑day path** to a compelling demo that converts “company + persona” into a **one‑page insight brief (5 items)** and a **compliant outreach email draft**, anchored to real Salesforce sources.

## Prompt:
You are a senior AI platform and retrieval systems architect.
Based on the following notes and the plan above:

Day 1 — Data & Schema  
Inventory finalized; fetch 120 pages max; normalization + chunking complete; metadata dictionary frozen.  
Milestones: ≥ 80 docs with dates; dedupe done; link health 100%.  
Deliverables: Data inventory CSV, metadata dictionary, normalization rules.

Please generate an **extremely detailed and comprehensive plan** (no code required). The plan should be so thorough that I can hand it directly to another model and have it generate the necessary code.

Requirements:

1. **Intended Use**

   * I will give your plan directly to another model so that it can implement it in code.
   * Therefore, your plan must be fully executable and leave no ambiguity.

2. **Structured and Complete**

   * Break down the process step by step, with clear goals, inputs, and outputs.
   * Instead of vague instructions like “fetch data,” explicitly describe:

     * Which data sources to use.
     * File naming conventions.
     * Corresponding Python script names (e.g., fetch_xxx.py).
     * The role of each script.
     * What files/artifacts they generate.

3. **Concrete Data Design**

   * Specify exactly what data to select, the scale, and the format.
   * Include **direct data links** (e.g., public datasets, download URLs, APIs) so that code can fetch the data automatically.
   * Clearly describe how each dataset will be used in the MVP, and how different files depend on one another.

4. **Evaluation & Verification**

   * The plan must include a well-designed **evaluation dataset**, not just raw extracted data.
   * Describe how the eval set is built:

     * What types of questions are included.
     * Expected answers and labels.
     * How pairs are matched.
     * Which use cases are covered.
   * The goal is to allow the model to answer questions and compare outputs against labels for measurable evaluation.

5. **Deliverables**

   * List all expected deliverables (e.g., CSVs, JSON files, metadata dictionary, normalization rules, evaluation datasets).
   * Explain how each deliverable connects to later stages in the workflow.

**Summary**:
Do not give me a generic or high-level plan. Instead, create a **blueprint that directly specifies files, data links, scripts, processing flows, and evaluation design**, ensuring that every step from data fetching to evaluation has a concrete and actionable path.

## Response:
Request for GPT-5 Pro

Reasoned for 10m 2s

Below is a **fully specified Day‑1 blueprint** you can hand to an implementation model. It is precise about **files, directories, script names, inputs/outputs, data links, metadata, normalization rules, chunking, dedupe, evaluation set design, and acceptance checks**. No code is included; every step is implementation‑ready.

* * *

0) Day‑1 Objective (what “done” means)
--------------------------------------

*   **Scope:** Salesforce, Inc. (NYSE: CRM) public materials only.
*   **Cap:** **≤ 120** pages fetched.
*   **Milestones:** **≥ 80** distinct documents with valid **publish/filing dates**; **dedupe complete**; **link health 100%** (HTTP 200 after redirects).
*   **Deliverables (Day‑1):**
    1.  **Data inventory CSV** (document‑level).
    2.  **Metadata dictionary** (frozen).
    3.  **Normalization rules** (frozen, per source).
    4.  **Raw/normalized/chunked artifacts** saved to disk.
    5.  **Eval seed set** (question/label JSONL) to verify retrieval readiness.
    6.  **Day‑1 verification report** (counts, coverage, link health, dedupe stats).

* * *

1) Repository layout & naming conventions
-----------------------------------------

```
repo_root/
  configs/
    sources.salesforce.yaml
    normalization.rules.yaml
    metadata.dictionary.yaml
    chunking.config.json
    eval.prompts.yaml
  scripts/
    fetch_sec_filings.py
    fetch_investor_news.py
    fetch_newsroom_rss.py
    fetch_product_docs.py
    fetch_dev_docs.py
    fetch_help_docs.py
    fetch_wikipedia.py
    normalize_html.py
    parse_sec_structures.py
    extract_metadata.py
    chunk_documents.py
    dedupe_chunks.py
    link_health_check.py
    build_eval_seed.py
    verify_day1_milestones.py
  data/
    raw/
      sec/
      investor_news/
      newsroom/
      product/
      dev_docs/
      help_docs/
      wikipedia/
    interim/
      normalized/
      chunks/
      dedup/
      eval/
    final/
      inventory/
      dictionaries/
      rules/
      reports/
  logs/
    fetch/
    normalize/
    chunk/
    dedupe/
    eval/
  README_DAY1.md
```

**ID conventions**

*   **doc\_id:** `crm::<doctype>::<yyyy-mm-dd>::<slug>::<sha1-8>`
    *   Examples:
        *   `crm::10-K::2025-03-05::annual-report::a1b2c3d4`
        *   `crm::press::2025-02-24::salesforce-and-google-gemini::9f8e7d6c`
*   **chunk\_id:** `<doc_id>::chunk<zero-padded-4>` (e.g., `::chunk0007`).

**File formats**

*   **Raw page artifact:** `data/raw/<source>/<doc_id>.raw.html` (or `.pdf`/`.json`)
*   **Normalized doc record:** JSONL at `data/interim/normalized/<doc_id>.json` (one JSON object)
*   **Chunks:** JSONL at `data/interim/chunks/<doc_id>.chunks.jsonl` (one line per chunk)
*   **Dedup mapping:** `data/interim/dedup/dedup_map.json`
*   **Inventory CSV:** `data/final/inventory/salesforce_inventory.csv`
*   **Eval seed set:** `data/interim/eval/salesforce_eval_seed.jsonl`
*   **Verification report:** `data/final/reports/day1_verification.json`

* * *

2) Source list & concrete links (fixed and crawlable)
-----------------------------------------------------

**Rationale:** These sources are **stable, authoritative**, and cover filings, investor updates, newsroom PR, product pages, docs, and background.

| Source | Type | How to collect | Time window | Target count | Link(s) |
| --- | --- | --- | --- | --- | --- |
| EDGAR entity browse (CIK 0001108524) | Index | Manual pick of specific filings below | 2024‑01‑01 → present | — | [SEC](https://www.sec.gov/edgar/browse/?CIK=0001108524&utm_source=chatgpt.com) |
| **FY25 Form 10‑K** (filed 2025‑03‑05) | 10‑K | Direct | n/a | 1 | [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com) |
| **FY26 Q1 10‑Q** (period ended 2025‑04‑30; filed 2025‑06‑?) | 10‑Q | Direct | n/a | 1 | [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000030/crm-20250430.htm?utm_source=chatgpt.com) |
| **8‑K (2025‑02‑26)** – FY25 results | 8‑K | Direct | n/a | 1 | [SEC+1](https://www.sec.gov/ix?doc=%2FArchives%2Fedgar%2Fdata%2F1108524%2F000110852425000002%2Fcrm-20250226.htm&utm_source=chatgpt.com) |
| **8‑K (2025‑05‑28)** – Q1 FY26 results | 8‑K | Direct | n/a | 1 | [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000027/crm-20250528.htm?utm_source=chatgpt.com) |
| **Annual Report to Holders (FY25) PDF** | ARS/PDF | Direct | n/a | 1 | [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000019/salesforce_fy25annualreport.pdf?utm_source=chatgpt.com) |
| **Proxy/Meeting results 2025‑06‑05** | 8‑K | Direct | n/a | 1 | [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000033/crm-20250605.htm?utm_source=chatgpt.com) |
| Investor Relations — News | Investor PR | Crawl listing for 2025; follow item links | 2024‑01‑01 → present | **20** | [Salesforce Investor Relations+1](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com) |
| Newsroom — **Corporate PR RSS** | PR (RSS) | Parse feed; fetch linked items | 2024‑01‑01 → present | **15** | [Salesforce](https://www.salesforce.com/news/content-types/press-releases-corporate/feed/?utm_source=chatgpt.com) |
| Newsroom — **Product PR RSS** | PR (RSS) | Parse feed; fetch linked items | 2024‑01‑01 → present | **15** | [Salesforce](https://www.salesforce.com/news/content-types/press-releases-product/feed/?utm_source=chatgpt.com) |
| Newsroom — **All News & Press** | PR index | Crawl first 20 linked articles (if accessible w/o JS) | 2024‑01‑01 → present | **20** | [Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com) |
| **Agentforce** product page | Product | Direct | Current | 1 | [Salesforce](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com) |
| **Data Cloud** product page | Product | Direct | Current | 1 | [Salesforce](https://www.salesforce.com/data/?utm_source=chatgpt.com) |
| **What is Salesforce?** | Product/Overview | Direct | Current | 1 | [Salesforce](https://www.salesforce.com/products/what-is-salesforce/?utm_source=chatgpt.com) |
| **Agent API** — Get started | Dev docs | Direct | Current | 1 | [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com) |
| **Agent API** — Guide | Dev docs | Direct | Current | 1 | [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api.html?utm_source=chatgpt.com) |
| **Agent API examples** | Dev docs | Direct | Current | 1 | [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-examples.html?utm_source=chatgpt.com) |
| **Get started with Agentforce Agents** | Dev docs | Direct | Current | 1 | [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/get-started-agents.html?utm_source=chatgpt.com) |
| **Agentforce: Agents & Copilot (Help)** | Help docs | Direct | Current | 1 | [Salesforce](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5&utm_source=chatgpt.com) |
| **Wikipedia: Salesforce** | Background | Direct | Current | 1 | [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com) |

**Expected page total:** ~**82–100** (stop when hitting **≥ 80** docs with dates and before **120** cap).

* * *

3) Concrete data design
-----------------------

### 3.1 Document record (normalized) — field spec (frozen Day‑1)

**Required fields (must be present in ≥ 98% of docs):**

*   `doc_id` (string; format above)
*   `company` (literal `"Salesforce"`)
*   `doctype` (enum: `10-K|10-Q|8-K|press|blog|product|dev_docs|help_docs|wiki|ars_pdf`)
*   `title` (string)
*   `publish_date` (ISO‑8601 `YYYY-MM-DD`) — **for SEC filings, use SEC “filed” date**; for PR/blog/docs, use page‑level `article:published_time`/visible date; fallback described in §5.
*   `url` (canonical URL)
*   `source_domain` (e.g., `sec.gov`, `investor.salesforce.com`, `salesforce.com`, `developer.salesforce.com`, `help.salesforce.com`, `wikipedia.org`)
*   `section` (string; for SEC: e.g., `Item 1A`, `MD&A`; else: `body`)
*   `topic` (string; pipe‑separated tags, e.g., `Agentforce|Data Cloud|Earnings`)
*   `persona_tags` (list of strings; seed mapping from personas in `configs/eval.prompts.yaml`)
*   `language` (`en` expected; drop others)
*   `text` (UTF‑8, normalized plain text)
*   `word_count` (int)
*   `token_count` (int; **cl100k\_base** tokenizer)
*   `ingestion_ts` (ISO‑8601 timestamp)
*   `hash_sha256` (hex)

**Optional fields:**

*   `html_title`, `meta_published_time`, `last_modified_http`, `byline`, `press_location`, `ticker_mentions[]`.

### 3.2 Chunk record — field spec (frozen Day‑1)

*   `chunk_id`, `doc_id`, `seq_no` (0‑based),
*   `text`, `word_count`, `token_count`,
*   `start_char`, `end_char`,
*   `local_heads[]` (nearest headings),
*   `metadata_snapshot` (inline copy of key doc metadata: `doctype,date,topic,url,title,company,persona_tags`).

### 3.3 Metadata dictionary (deliverable, formalized in `configs/metadata.dictionary.yaml`)

For each field above: **type**, **allowed values**, **fill rule precedence**, **validation regex**, **examples**, **nullability**, **owner script**.

* * *

4) Scripts (exact names, purpose, inputs, outputs)
--------------------------------------------------

> All scripts must accept `--dry-run` (no writes), `--limit N`, `--since YYYY-MM-DD`, `--until YYYY-MM-DD`, and `--concurrency K` flags, and write logs to `logs/<stage>/YYYYMMDD_HHMMSS.log`.

### 4.1 Fetchers (raw acquisition)

1.  **`fetch_sec_filings.py`**
    *   **Role:** Download specific Salesforce filings listed in §2 (HTML and linked PDF).
    *   **Inputs:** Hardcoded list of SEC URLs (from §2); `--limit` for safety.
    *   **Outputs:** `data/raw/sec/<doc_id>.raw.html` (or `.pdf` for ARS), plus `data/raw/sec/<doc_id>.meta.json` (filing date, form type from page header).
    *   **Rules:** **Rate ≤ 6 req/s**, follow redirects, preserve original filename in meta.
2.  **`fetch_investor_news.py`**
    *   **Role:** Crawl **Investor News** listing page(s), collect items **2024‑01‑01 → present**, fetch article pages.
    *   **Start URL:** [https://investor.salesforce.com/news/default.aspx](https://investor.salesforce.com/news/default.aspx?utm_source=chatgpt.com) (may include `?languageid=1`). [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)
    *   **Link discovery:** On listing pages, collect anchors under lists/blocks whose `href` contains `/news/` and page dates within window.
    *   **Outputs:** Raw HTML at `data/raw/investor_news/<doc_id>.raw.html` and `meta.json` per doc with `visible_date`, `headline`.
    *   **Stop:** **20** article pages or when date bound reached.
3.  **`fetch_newsroom_rss.py`**
    *   **Role:** Parse RSS feeds and fetch linked newsroom items.
    *   **Feeds:**
        *   Corporate PR RSS: [https://www.salesforce.com/news/content-types/press-releases-corporate/feed/](https://www.salesforce.com/news/content-types/press-releases-corporate/feed/?utm_source=chatgpt.com) [Salesforce](https://www.salesforce.com/news/content-types/press-releases-corporate/feed/?utm_source=chatgpt.com)
        *   Product PR RSS: [https://www.salesforce.com/news/content-types/press-releases-product/feed/](https://www.salesforce.com/news/content-types/press-releases-product/feed/) [Salesforce](https://www.salesforce.com/news/content-types/press-releases-product/feed/?utm_source=chatgpt.com)
    *   **Window:** **2024‑01‑01 → present**; fetch latest **30** total (≈15 each).
    *   **Outputs:** `data/raw/newsroom/<doc_id>.raw.html` and `meta.json` with `rss_pubdate`.
4.  **`fetch_product_docs.py`**
    *   **Role:** Fetch product/overview pages.
    *   **URLs:**
        *   Agentforce: [https://www.salesforce.com/agentforce/](https://www.salesforce.com/agentforce/) [Salesforce](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com)
        *   Data Cloud: [https://www.salesforce.com/data/](https://www.salesforce.com/data/) [Salesforce](https://www.salesforce.com/data/?utm_source=chatgpt.com)
        *   What is Salesforce: [https://www.salesforce.com/products/what-is-salesforce/](https://www.salesforce.com/products/what-is-salesforce/?utm_source=chatgpt.com) [Salesforce](https://www.salesforce.com/products/what-is-salesforce/?utm_source=chatgpt.com)
    *   **Outputs:** `data/raw/product/<doc_id>.raw.html` + `meta.json`.
5.  **`fetch_dev_docs.py`**
    *   **Role:** Fetch developer docs (Agent API).
    *   **URLs:**
        *   Get Started: [https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html) [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)
        *   API Guide: [https://developer.salesforce.com/docs/einstein/genai/guide/agent-api.html](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api.html) [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api.html?utm_source=chatgpt.com)
        *   Examples: [https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-examples.html](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-examples.html) [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-examples.html?utm_source=chatgpt.com)
        *   Agents overview: [https://developer.salesforce.com/docs/einstein/genai/guide/get-started-agents.html](https://developer.salesforce.com/docs/einstein/genai/guide/get-started-agents.html) [Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/get-started-agents.html?utm_source=chatgpt.com)
    *   **Outputs:** `data/raw/dev_docs/<doc_id>.raw.html` + `meta.json`.
6.  **`fetch_help_docs.py`**
    *   **Role:** Fetch Agentforce help page.
    *   **URL:** [https://help.salesforce.com/s/articleView?id=sf.copilot\_intro.htm&language=en\_US&type=5](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5) [Salesforce](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5&utm_source=chatgpt.com)
    *   **Outputs:** `data/raw/help_docs/<doc_id>.raw.html` + `meta.json`.
7.  **`fetch_wikipedia.py`**
    *   **Role:** Fetch Wikipedia company page.
    *   **URL:** [https://en.wikipedia.org/wiki/Salesforce](https://en.wikipedia.org/wiki/Salesforce) [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)
    *   **Outputs:** `data/raw/wikipedia/<doc_id>.raw.html` + `meta.json` with `last_modified_http`.

### 4.2 Normalization & metadata extraction

8.  **`normalize_html.py`**
    *   **Role:** Convert raw HTML/PDF to clean UTF‑8 text; strip boilerplate; harmonize whitespace.
    *   **Inputs:** `data/raw/**/<doc_id>.raw.*`
    *   **Outputs:** `data/interim/normalized/<doc_id>.json` (document record per §3.1 with text filled; temporary missing metadata allowed).
    *   **Boilerplate strip rules (global):**
        *   Remove nav, footer, cookie banners, TOC menus, “share” bars, and repetitive sidebars.
        *   Collapse 2+ spaces/newlines. Preserve headings (H1–H3).
        *   For PDFs: extract text in reading order; store `pdf_page_map[]` if available.
    *   **Language:** detect via a standard library; drop non‑English.
9.  **`parse_sec_structures.py`**
    *   **Role:** For SEC filings, segment **Items** and fill `section`.
    *   **Inputs:** normalized SEC docs.
    *   **Rules:** Regex‑based anchors:
        *   `Item 1\.` → Business; `Item 1A\.` → Risk Factors; `Item 7\.` → MD&A; `Item 7A\.` → Market Risk; `Item 8\.` → Financial Statements.
    *   **Outputs:** update normalized doc JSON with `section="Item X"` per text span mapping (store spans for chunker).
10.  **`extract_metadata.py`**
    *   **Role:** Populate required metadata fields consistently.
    *   **Inputs:** normalized documents; source‑specific parsers.
    *   **Date precedence:**
        1.  SEC: filing header (visible “Filed” date). (If absent, use EDGAR index meta.) [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
        2.  Investor/newsroom: `<meta property="article:published_time">` or visible dateline. [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)[Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
        3.  Product/docs/help: visible “Updated” date; else HTTP `Last-Modified`. [Salesforce Developers+1](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)[Salesforce](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5&utm_source=chatgpt.com)
        4.  Wikipedia: page info (`last-modified`) header. [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)
    *   **Title precedence:** `<meta property="og:title">` → `<title>` → `<h1>`.
    *   **Topic tags:** rule‑based from headings and keyword lexicons (e.g., `Agentforce`, `Data Cloud`, `Earnings`, `Partnership`).
    *   **Persona tags:** map via `configs/eval.prompts.yaml` (e.g., `vp_customer_experience` → keywords like `NPS|CSAT|contact center|agent productivity`).
    *   **Outputs:** overwrite/update each `data/interim/normalized/<doc_id>.json`.

### 4.3 Chunking, dedupe, link health

11.  **`chunk_documents.py`**
    *   **Role:** Produce semantic chunks for retrieval.
    *   **Inputs:** normalized JSON.
    *   **Config:** `configs/chunking.config.json`
        *   `target_tokens=800`, `overlap_tokens=120`, tokenizer=`cl100k_base`.
        *   Section‑aware splitting (SEC items and H2/H3 headings).
        *   For short docs `< 350 tokens`, emit **one** chunk.
    *   **Outputs:** `data/interim/chunks/<doc_id>.chunks.jsonl`.
12.  **`dedupe_chunks.py`**
    *   **Role:** Remove near‑duplicate chunks across all docs.
    *   **Method:** MinHash or SimHash; treat chunks **near‑duplicate if Jaccard ≥ 0.85** (shingle size=5 words).
    *   **Outputs:**
        *   `data/interim/dedup/dedup_map.json` with lists of `{canonical_chunk_id, duplicate_chunk_ids[]}`.
        *   Write filtered per‑doc chunk files in place (or to `data/interim/chunks/filtered/` if preferred).
    *   **Acceptance:** overall duplicate ratio **≤ 15%**; else log top offenders.
13.  **`link_health_check.py`**
    *   **Role:** Verify all `url` fields resolve to HTTP **200**.
    *   **Method:** **GET** (fallback **HEAD**), follow redirects; record `final_url`, `status_code`, `last_modified`.
    *   **Outputs:** update each normalized doc JSON with `final_url` & `link_ok=true`; write a summary at `data/final/reports/link_health.json`.
    *   **Requirement:** **100%** link\_ok; **0** broken links allowed Day‑1.
14.  **`build_eval_seed.py`**
    *   **Role:** Generate a **retrieval‑readiness evaluation dataset** (not model answers; ground‑truth pairs).
    *   **Inputs:** normalized docs + chunks.
    *   **Outputs:** `data/interim/eval/salesforce_eval_seed.jsonl` (spec in §7).
15.  **`verify_day1_milestones.py`**
    *   **Role:** Compute counts and checks for Day‑1 sign‑off.
    *   **Outputs:** `data/final/reports/day1_verification.json` with:
        *   `docs_with_dates`, `total_docs`, `chunks_total`, `duplicates_removed`, `link_ok_pct`, `by_doctype_counts`, `by_source_domain_counts`.

* * *

5) Normalization rules (frozen Day‑1)
-------------------------------------

**Global (all HTML):**

*   Remove elements by role/class if present: `nav`, `footer`, `[aria-label*="cookie"]`, `.share`, `.social`, `.newsletter`, `.breadcrumb`, `.sidebar` (if not content), `<script>`, `<style>`.
*   Preserve main content containers: prefer `<article>`, `main`, `.content`, `.entry-content`.
*   Replace `<br>`/`<p>` with newline; collapse multiple newlines to max 2.
*   Decode HTML entities; strip inline SVGs; remove tracking parameters from URLs (e.g., `?utm_*`).
*   Keep headings H1–H3.
*   Language detection: expect `en`; drop if not `en`.

**SEC (edgar `sec.gov` pages)**

*   Keep “Table of Contents” section titles but **drop navigation lists** that are repeated.
*   Segment by **Item** headers (`Item 1.`, `Item 1A.`, `Item 7.`, `Item 7A.`, `Item 8.`).
*   **publish\_date**: use **Filed** date from the filing page (e.g., FY25 10‑K dated March 2025; FY26 Q1 10‑Q April 30, 2025 period, filed June). [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
*   For PDF ARS, extract text and keep page numbers.

**Investor & Newsroom**

*   Extract visible dateline and headline. Investor News listing and article pages found under IR domain. [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)
*   For Newsroom feeds, **rss:pubDate** is primary; also parse article’s `meta` time if present. [Salesforce+1](https://www.salesforce.com/news/content-types/press-releases-corporate/feed/?utm_source=chatgpt.com)

**Product / Dev Docs / Help**

*   Keep product hero H1 and primary sections.
*   For dev docs/help, detect “Last updated” or version bands; otherwise rely on HTTP `Last-Modified`. [Salesforce Developers+1](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)[Salesforce](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5&utm_source=chatgpt.com)

**Wikipedia**

*   Keep lead section and first three section headings; strip infobox tables after converting key fields to text. [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)

* * *

6) Data inventory CSV (deliverable spec)
----------------------------------------

**Path:** `data/final/inventory/salesforce_inventory.csv`  
**Columns (order fixed):**

`doc_id, company, doctype, title, publish_date, url, final_url, source_domain, section, topic, persona_tags, language, word_count, token_count, ingestion_ts, hash_sha256`

**Population rules:**

*   `topic`: pipe‑separated tags (derived in `extract_metadata.py`)
*   `persona_tags`: comma‑separated (from persona mapping; may be empty)
*   `final_url`: from `link_health_check.py`
*   Validate **publish\_date present** for **≥ 98%** of rows.

* * *

7) Evaluation seed set (Day‑1) — design & build
-----------------------------------------------

**Purpose:** Enable automated, **quantitative Day‑2 retrieval sanity checks** without generation. The seed set contains **query → relevant passage** pairs.

**Path:** `data/interim/eval/salesforce_eval_seed.jsonl`  
**Record schema (one JSON object per line):**

*   `eval_id` (string; unique)
*   `persona` (enum: `vp_customer_experience|cio|vp_sales_ops`)
*   `query_text` (string)
*   `expected_doc_id` (string)
*   `expected_chunk_id` (string)
*   `expected_answer_keyphrases[]` (list of 2–5 canonical tokens to confirm match; e.g., `["Agentforce", "digital labor"]`)
*   `source_type` (enum mirroring `doctype`)
*   `created_from_url` (string)
*   `label_date` (ISO date; must be within doc’s date)
*   `difficulty` (`easy|medium|hard`)
*   `notes` (string; optional)

**How to build (performed by `build_eval_seed.py`):**

1.  **SEC facts (10 items):**
    *   From FY25 10‑K and FY26 Q1 10‑Q, extract 10 atomic facts: one **risk factor label**, one **revenue or margin figure**, one **segment definition**, one **RPO definition**, one **competition statement**, etc. Each fact maps to a single chunk (`expected_chunk_id`). [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
    *   **Queries**: natural language forms (e.g., “What does Salesforce define as Remaining Performance Obligation?”).
    *   **Persona:** `cio` and `vp_sales_ops` split.
2.  **Investor PR (10 items):**
    *   From IR news (2025), create Q for each of 10 items (e.g., “What did Salesforce announce on 2025‑03‑05 regarding Agentforce?”). Map to the press article chunk. [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)
    *   **Persona:** `vp_sales_ops`.
3.  **Newsroom PR (10 items):**
    *   From RSS‑fetched PR, create Qs (“Which airline co‑develops solutions with Salesforce?”) mapped to newsroom chunks. [Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
4.  **Product/Help/Dev docs (8 items):**
    *   Definitions (“What is Agentforce?”), capability Qs (“What does Data Cloud power?”), and API basics (“What endpoint starts an Agent session?” expected to match chunk containing intro). [Salesforce+1](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com)[Salesforce Developers](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)
    *   **Persona:** `vp_customer_experience` and `cio`.
5.  **Wikipedia background (2 items):**
    *   Foundational Qs (“When was Salesforce founded?”) mapped to wiki chunks; used to test diversity. [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)

**Seed set size:** **40** queries minimum.

**Verification for the seed set (Day‑1):**

*   Every record must have a resolvable `expected_doc_id` and `expected_chunk_id`.
*   `expected_answer_keyphrases[]` must appear in that chunk’s text (string‑contains).
*   Dates within **24 months** for PR (where applicable).

* * *

8) Chunking parameters (frozen Day‑1)
-------------------------------------

*   **Tokenizer:** `cl100k_base` (count only; no model calls).
*   **Window:** **800 tokens** with **120 overlap**.
*   **Title boost:** include `title` and top‑level heading at the top of **chunk 0**.
*   **Short‑doc rule:** if `token_count < 350`, produce a single chunk.
*   **SEC sections:** reset chunk sequence at each `Item` boundary.

* * *

9) Dedupe parameters (frozen Day‑1)
-----------------------------------

*   **Shingling:** 5‑word shingles, case‑folded, punctuation‑stripped.
*   **Near‑duplicate if Jaccard ≥ 0.85** (or SimHash Hamming distance ≤ 3 on 64‑bit).
*   **Canonical selection:** choose the earliest `publish_date`; tie‑break: longer `word_count`.
*   **Retention:** keep canonical, discard duplicates; map duplicates in `dedup_map.json`.
*   **Report:** top 10 source domains by duplicate ratio.

* * *

10) Link health (frozen Day‑1)
------------------------------

*   **HTTP method:** `GET` (with 5s timeout). Fallback `HEAD`.
*   **Redirects:** follow up to 5 hops; record `final_url`.
*   **Success:** `status_code` in {200}.
*   **Failure policy:** **No failures allowed**. If any fail, re‑try with exponential backoff (up to 3 attempts) and then mark Day‑1 “not met”.

* * *

11) Persona mapping (Day‑1 seed)
--------------------------------

**`configs/eval.prompts.yaml`** must include:

*   **Personas:**
    *   `vp_customer_experience`: keywords `NPS, CSAT, contact center, omnichannel, agent productivity, self‑service, first contact resolution`
    *   `cio`: `data integration, governance, security, TCO, platform, APIs, real‑time`
    *   `vp_sales_ops`: `pipeline, forecast accuracy, win rate, productivity, automation`

Scripts use these to populate `persona_tags` and to construct evaluation queries.

* * *

12) Quality gates & acceptance checks (Day‑1)
---------------------------------------------

*   **Coverage:** `total_docs ≥ 80` **with `publish_date` present**.
*   **Cap:** `total_fetched ≤ 120`.
*   **Dedup:** duplicate ratio ≤ **15%** (by chunks).
*   **Link health:** **100%** of docs pass.
*   **Metadata completeness:** required fields present in **≥ 98%** of normalized docs.
*   **Recency:** for PR (investor/newsroom), at least **15** docs dated **≥ 2024‑01‑01** and **≥ 8** within **last 12 months**.
*   **Inventory CSV validation:** row count equals number of normalized docs; all `doc_id` unique.

`verify_day1_milestones.py` must compute and persist these to `data/final/reports/day1_verification.json`:

```text
{
  "total_docs": INT,
  "docs_with_dates": INT,
  "chunks_total": INT,
  "duplicates_removed": INT,
  "link_ok_pct": FLOAT,
  "by_doctype_counts": { "10-K": INT, "10-Q": INT, ... },
  "by_source_domain_counts": { "sec.gov": INT, ... },
  "pr_docs_last_12mo": INT
}
```

* * *

13) How Day‑1 artifacts connect to later stages
-----------------------------------------------

*   **Inventory CSV** → used by **indexers** (Day‑2) to build Pinecone/Weaviate/FAISS metadata.
*   **Normalized docs** → source of truth for **embedding & chunking**; chunk files feed the **multi‑vector index build**.
*   **Metadata dictionary** → enforces stable schemas for LangGraph and MCP tool payloads.
*   **Normalization rules** → reproducible fetch/parse, required for auditability and compliance.
*   **Eval seed set** → used on Day‑2/Day‑4 to compute **Recall@k, nDCG@k** and verify router.
*   **Link health report** → prevents dead citations in later **insight cards**.

* * *

14) Detailed execution order for Day‑1
--------------------------------------

1.  **Create configs**
    *   Write `configs/sources.salesforce.yaml` with the exact URLs/feeds from §2 and per‑source limits.
    *   Freeze `configs/metadata.dictionary.yaml`, `configs/normalization.rules.yaml`, `configs/chunking.config.json`, `configs/eval.prompts.yaml`.
2.  **Run fetchers in this order**  
    a) `fetch_sec_filings.py` (6–7 filings including ARS PDF).  
    b) `fetch_investor_news.py` (`--since 2024-01-01 --limit 30` but stop at 20 valid articles with dates).  
    c) `fetch_newsroom_rss.py` (target 30 articles, 15 corporate + 15 product).  
    d) `fetch_product_docs.py` (3 URLs).  
    e) `fetch_dev_docs.py` (4 URLs).  
    f) `fetch_help_docs.py` (1 URL).  
    g) `fetch_wikipedia.py` (1 URL).
3.  **Normalize & extract metadata**  
    a) `normalize_html.py` over all raw artifacts.  
    b) `parse_sec_structures.py` for SEC docs.  
    c) `extract_metadata.py` (fill dates, titles, topics, persona\_tags).
4.  **Chunking & dedupe**  
    a) `chunk_documents.py` (expect ~2,500–5,000 chunks for 80–100 docs).  
    b) `dedupe_chunks.py` (produce `dedup_map.json` and filtered chunk files).
5.  **Link health**
    *   `link_health_check.py` → **100%** pass.
6.  **Inventory & eval seed**
    *   Generate `salesforce_inventory.csv` from normalized docs.
    *   Run `build_eval_seed.py` to create 40 Q‑pairs in `salesforce_eval_seed.jsonl`.
7.  **Verification**
    *   `verify_day1_milestones.py` → `day1_verification.json`.
    *   If any gate fails, fix and rerun relevant script before sign‑off.

* * *

15) Normalization & topic tagging specifics (per source)
--------------------------------------------------------

*   **SEC (10‑K/10‑Q/8‑K/ARS):**
    *   `doctype`: `10-K` / `10-Q` / `8-K` / `ars_pdf` as applicable.
    *   `topic`: from section headers (e.g., `Risk Factors`, `MD&A`, `Earnings`).
    *   `title`: `<h1>` or document caption (e.g., “FORM 10‑K”).
    *   `publish_date`: filing date (visible on page). [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
*   **Investor News (IR):**
    *   `doctype`: `press`.
    *   `topic`: parse from title; constrain to tags: `Earnings|Partnership|Product|Customer Story|Executive`.
    *   `publish_date`: visible date on article page. [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)
*   **Newsroom PR (RSS):**
    *   `doctype`: `press`.
    *   `publish_date`: RSS `pubDate` → convert to ISO date; cross‑check article. [Salesforce+1](https://www.salesforce.com/news/content-types/press-releases-corporate/feed/?utm_source=chatgpt.com)
*   **Product pages:**
    *   `doctype`: `product`.
    *   `topic`: e.g., `Agentforce`, `Data Cloud`. [Salesforce+1](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com)
*   **Dev docs:**
    *   `doctype`: `dev_docs`.
    *   `topic`: e.g., `Agent API`. [Salesforce Developers+1](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)
*   **Help docs:**
    *   `doctype`: `help_docs`. [Salesforce](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5&utm_source=chatgpt.com)
*   **Wikipedia:**
    *   `doctype`: `wiki`. [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)

* * *

16) Data selection scale (exact)
--------------------------------

*   **SEC:** 6–7 documents.
*   **IR news:** 20 articles (2024–2025).
*   **Newsroom PR:** 30 articles via RSS (15 corporate + 15 product).
*   **All News & Press index:** up to 20 if accessible without JS; skip if dynamic (replace with extra IR items to keep total ≤ 120). [Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
*   **Product + Docs + Help + Wikipedia:** 10 pages.
*   **Total:** ~86–107; stop at **≥ 80** with dates.

* * *

17) Day‑1 Deliverables (explicit file list)
-------------------------------------------

*   `data/final/inventory/salesforce_inventory.csv` (document‑level inventory).
*   `configs/metadata.dictionary.yaml` (frozen field definitions).
*   `configs/normalization.rules.yaml` (frozen rules per source).
*   `configs/chunking.config.json` (800/120 tokens, tokenizer id).
*   `data/interim/normalized/*.json` (one per doc).
*   `data/interim/chunks/*.chunks.jsonl` (one per doc).
*   `data/interim/dedup/dedup_map.json` (canonical→dupes).
*   `data/interim/eval/salesforce_eval_seed.jsonl` (40+ query‑label pairs).
*   `data/final/reports/link_health.json` (all URLs OK).
*   `data/final/reports/day1_verification.json` (gates & stats).
*   `README_DAY1.md` (how to run Day‑1 pipeline, script order, acceptance thresholds).

* * *

18) Day‑1 verification checklist (must be satisfied)
----------------------------------------------------

1.  **Counts:** `total_docs ≥ 80` with `publish_date` present; `≤ 120` fetched.
2.  **Dedup:** Jaccard ≥ 0.85 duplicates removed; ratio ≤ 15%.
3.  **Link health:** 100% pass; `final_url` set.
4.  **Inventory CSV:** valid schema; `doc_id` unique; `source_domain` only from allowed set.
5.  **Eval seed set:** ≥ 40 items; each pair’s `expected_chunk_id` text contains all `expected_answer_keyphrases`.

* * *

19) Risks & mitigations (Day‑1 specific)
----------------------------------------

*   **Dynamic newsroom “load more”:** If [https://www.salesforce.com/news/all-news-press-salesforce/](https://www.salesforce.com/news/all-news-press-salesforce/) requires JS, rely on RSS feeds + Investor News to reach counts. [Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
*   **SEC HTML variability:** Use regex section detection; if section tagging fails, still index full text with `section="body"`. [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
*   **Date missing on IR items:** Fallback to HTTP `Last-Modified`; if still missing, **exclude** from final inventory to preserve ≥ 98% date completeness. [Salesforce Investor Relations](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)
*   **Rate limits:** throttle to **≤ 6 rps**, exponential backoff.
*   **PDF extraction noise (ARS):** accept lower chunk quality; use as secondary source. [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000019/salesforce_fy25annualreport.pdf?utm_source=chatgpt.com)

* * *

20) Acceptance note for handoff
-------------------------------

When this plan is executed:

*   You will have a **normalized, dated corpus (≥ 80 docs)** of Salesforce filings, PR, product pages, docs, help, and Wikipedia, with **chunked & deduped** text and a **seed evaluation set**.
*   All artifacts are named and stored predictably for **Day‑2 indexing** (Pinecone/Weaviate/FAISS), **Day‑3 LangGraph**, and **Day‑4 evaluation**.

If anything blocks (e.g., a link goes offline), replace the failed item with another 2024–2025 IR or Newsroom item to maintain counts without exceeding the cap.

* * *

### Source anchors cited above

*   **EDGAR browse:** Salesforce CIK 0001108524. [SEC](https://www.sec.gov/edgar/browse/?CIK=0001108524&utm_source=chatgpt.com)
*   **FY25 10‑K:** crm‑20250131. [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm?utm_source=chatgpt.com)
*   **FY26 Q1 10‑Q:** crm‑20250430. [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000030/crm-20250430.htm?utm_source=chatgpt.com)
*   **8‑K Feb 26, 2025:** FY25 results. [SEC+1](https://www.sec.gov/ix?doc=%2FArchives%2Fedgar%2Fdata%2F1108524%2F000110852425000002%2Fcrm-20250226.htm&utm_source=chatgpt.com)
*   **8‑K May 28, 2025:** Q1 results. [SEC](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000027/crm-20250528.htm?utm_source=chatgpt.com)
*   **FY25 Annual Report (PDF):** ARS. [SEC+1](https://www.sec.gov/Archives/edgar/data/1108524/000110852425000019/salesforce_fy25annualreport.pdf?utm_source=chatgpt.com)
*   **Investor News list:** IR portal. [Salesforce Investor Relations+1](https://investor.salesforce.com/news/default.aspx?languageid=1&utm_source=chatgpt.com)
*   **Newsroom All News & Press:** index. [Salesforce](https://www.salesforce.com/news/all-news-press-salesforce/?utm_source=chatgpt.com)
*   **RSS feeds (Corporate/Product):** newsroom feeds. [Salesforce+1](https://www.salesforce.com/news/content-types/press-releases-corporate/feed/?utm_source=chatgpt.com)
*   **Product pages:** Agentforce, Data Cloud, What is Salesforce. [Salesforce+2Salesforce+2](https://www.salesforce.com/agentforce/?utm_source=chatgpt.com)
*   **Dev docs:** Agent API pages. [Salesforce Developers+2Salesforce Developers+2](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html?utm_source=chatgpt.com)
*   **Help docs:** Agentforce help. [Salesforce](https://help.salesforce.com/s/articleView?id=sf.copilot_intro.htm&language=en_US&type=5&utm_source=chatgpt.com)
*   **Wikipedia:** Salesforce. [Wikipedia](https://en.wikipedia.org/wiki/Salesforce?utm_source=chatgpt.com)

This is everything a coding model needs to implement Day‑1 **Data & Schema** for the Account Research & Outreach Studio MVP.

## Prompt:
I have written the code according to your request, and  the output is in the end. how can I  design an additional testing procedure to evaluate whether the data obtained by the code fully meets your requirements?

If possible, I would like you to provide me with a plan similar to the one you gave before. I don’t need new code; instead, I would like you to follow the previous requirements and generate a detailed plan on how I should check the quality of the current dataset.

At present, I’ve noticed one shortcoming: the duplication rate does not meet the 15% standard. However, I am also concerned that there may be other issues, such as incorrect extraction or garbled text. In addition to the examples I’ve mentioned, please also include other quality checks that you think are important, and design the overall evaluation plan accordingly.

##Output
“”“” All core Day‑1 artifacts and scripts are in place. Here’s what I added and how to run. Repo Setup Configs: frozen rules, sources, dictionary, chunking, personas. configs/sources.salesforce.yaml:1 configs/normalization.rules.yaml:1 configs/metadata.dictionary.yaml:1 configs/chunking.config.json:1 configs/eval.prompts.yaml:1 Utilities: shared helpers for logging, rate‑limit, HTTP, HTML→text, tokenization, IDs. scripts/_common.py:1 Fetchers: SEC, Investor IR, Newsroom RSS, Product, Dev Docs, Help, Wikipedia. scripts/fetch_sec_filings.py:1 scripts/fetch_investor_news.py:1 scripts/fetch_newsroom_rss.py:1 scripts/fetch_product_docs.py:1 scripts/fetch_dev_docs.py:1 scripts/fetch_help_docs.py:1 scripts/fetch_wikipedia.py:1 Normalization & Metadata: scripts/normalize_html.py:1 scripts/parse_sec_structures.py:1 scripts/extract_metadata.py:1 Chunking & Dedupe: scripts/chunk_documents.py:1 scripts/dedupe_chunks.py:1 Link Health, Eval Seed, Verification: scripts/link_health_check.py:1 scripts/build_eval_seed.py:1 scripts/verify_day1_milestones.py:1 Docs & deps: README_DAY1.md:1 requirements.txt:1 CLI & Logging All scripts support: --dry-run, --limit, --since, --until, --concurrency. Logs written to logs/<stage>/YYYYMMDD_HHMMSS.log (stages: fetch|normalize|chunk|dedupe|eval). I/O Conventions Raw: data/raw/<source>/<doc_id>.raw.html|.pdf + .meta.json per source. Normalized: data/interim/normalized/<doc_id>.json (document record). Chunks: data/interim/chunks/<doc_id>.chunks.jsonl and filtered dedupe: data/interim/chunks/filtered/… Dedupe map: data/interim/dedup/dedup_map.json Inventory: data/final/inventory/salesforce_inventory.csv Link health report: data/final/reports/link_health.json Day‑1 verification: data/final/reports/day1_verification.json Eval seed: data/interim/eval/salesforce_eval_seed.jsonl Highlights of Implementation SEC fetcher parses Filed date and form hints; writes PDF/HTML and meta. scripts/fetch_sec_filings.py:1 Investor IR crawler discovers /news/ links and parses <meta article:published_time> or visible date. scripts/fetch_investor_news.py:1 Newsroom via RSS (corporate + product); respects window/limit. scripts/fetch_newsroom_rss.py:1 Normalizer removes boilerplate per rules, keeps H1–H3, calculates word_count and token_count (cl100k_base if available; fallback heuristic). scripts/normalize_html.py:1 SEC sections segmented by regex (Item 1, 1A, 7, 7A, 8) with span annotations for chunker. scripts/parse_sec_structures.py:1 Metadata extraction applies precedence for publish_date, title, topics via lexicon, persona tags via keywords. scripts/extract_metadata.py:1, configs/eval.prompts.yaml:1 Chunking uses 800/120 window with short‑doc single chunk. scripts/chunk_documents.py:1, configs/chunking.config.json:1 Dedupe: 5‑word shingles + Jaccard ≥ 0.85; outputs canonical→dupes and filtered chunk files. scripts/dedupe_chunks.py:1 Link health: GET fallback HEAD with redirects; updates normalized JSON and writes report. scripts/link_health_check.py:1 Eval seed: samples 40+ pairs across chunks with templated queries and keyphrases from chunk text. scripts/build_eval_seed.py:1 Verification: writes inventory CSV and Day‑1 report with all required counts. scripts/verify_day1_milestones.py:1 How To Run Install deps (optional libs auto‑detected; scripts degrade gracefully): python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt Execute in order (dry‑run first) as outlined in README_DAY1.md:1. Notes/Assumptions Token counting uses tiktoken if installed; otherwise a conservative heuristic. Investor IR listing parsing is HTML‑based (no JS); if listing is dynamic, rely on Newsroom RSS + more IR pages as needed to hit counts. SEC Filed date parsing is robust to common patterns; normalization/metadata extractor will backfill if needed from raw meta. Dedupe uses O(n^2) Jaccard for Day‑1 scale; acceptable for ~5k chunks. Ran everything in your conda env using conda run -n age (never in base). Summary below with key results and artifacts. What I Ran Env: conda run -n age python3 ... for all installs and scripts. Deps: requirements.txt installed into age. Fetch → Normalize → Parse SEC → Metadata → Chunk → Dedupe → Link health → Eval → Verify, plus a newsroom index crawler to reach counts. Day‑1 Results Total docs: 97 (publish_date present: 97) — within ≤ 120 cap. Link health: 100% (97/97). Chunks: 1,734 pre‑dedupe; 365 duplicates removed; 1,368 kept. By doctype: press 82; SEC 10‑K 1; 10‑Q 1; 8‑K 3; product 3; dev_docs 4; help_docs 1; ars_pdf 1; wiki 1. PR recency: 82 in last 12 months. Eval seed: 40 items. Outputs Inventory CSV: data/final/inventory/salesforce_inventory.csv Normalized docs: data/interim/normalized/*.json Chunks (raw/filtered): data/interim/chunks/*.chunks.jsonl, data/interim/chunks/filtered/*.chunks.jsonl Dedupe map: data/interim/dedup/dedup_map.json Link health: data/final/reports/link_health.json Day‑1 verification: data/final/reports/day1_verification.json Eval seed: data/interim/eval/salesforce_eval_seed.jsonl Logs: logs/*/* (fetch/normalize/chunk/dedupe/eval) Notes To meet counts, I added scripts/fetch_newsroom_index.py (non‑JS index crawl, first 20–40 links) and a fallback XML parser in fetch_newsroom_rss.py. I also increased RSS target_count_total to 60 in configs/sources.salesforce.yaml. Robustness fixes: added PyYAML; made dedupe and eval seed resilient to malformed/empty lines. Open Item (Dedupe Ratio) Dedupe removed ~21% of chunks (365/1734), above the ≤ 15% target, likely due to residual boilerplate on newsroom pages being near‑identical. If you want, I can: Tighten normalization to drop repeated newsroom footers/CTAs, or Ignore shingles that occur in ≥ M docs, or Raise Jaccard threshold slightly (e.g., 0.90) to lower duplicate detections. “”“

## Response:
Request for GPT-5 Pro

Reasoned for 6m 23s

Below is a **fully specified QA & dataset‑validation blueprint** you can hand directly to a coding model to implement your **Day‑1 dataset testing procedure**. It is structured like the previous plans (no code) and is tailored to the issues you flagged (notably, **duplicate rate > 15%**) while also guarding against **incorrect extraction, garbled text, missing/incorrect dates, sectioning errors, and coverage gaps**.

* * *

0) QA Objective & Acceptance
----------------------------

**Goal:** Prove that the Day‑1 corpus **meets or exceeds** all data quality requirements before Day‑2 indexing. Detect, localize, and explain failures with actionable remediation artifacts.

**Global pass criteria (must all be satisfied):**

*   **Docs with dates:** ≥ **80** and **≥ 98%** of normalized docs have valid `publish_date`.
*   **Link health:** **100%** of `url` → `final_url` resolve to HTTP 200.
*   **Deduplication:** **≤ 15%** near‑duplicate **after boilerplate removal**; plus **≤ 5%** exact duplicates (hash‑identical) at the **document** level.
*   **Text quality:**
    *   `garbled_text_flag = false` for **≥ 99%** of chunks,
    *   printable ratio ≥ **0.995**,
    *   “replacement char” `�` count = **0** in **≥ 99%** of docs.
*   **SEC sectioning:** For each SEC 10‑K/10‑Q, **all of** `Item 1, 1A, 7, 7A, 8` detected with **correct order**; section boundary crossing in chunks = **0**.
*   **Metadata completeness:** Required fields filled in **≥ 98%** of normalized docs.
*   **Coverage:**
    *   PR dated within last 12 months: **≥ 8** docs,
    *   SEC: at least **1** 10‑K + **1** 10‑Q + **1** 8‑K present.
*   **Eval seed integrity:** **≥ 40** query→chunk pairs; for each pair, **all** `expected_answer_keyphrases[]` appear in `expected_chunk_id`.

> If any criterion fails, produce focused remediation artifacts (see §8), re‑run QA, then sign off.

* * *

1) QA Repository Layout & Naming
--------------------------------

Add a new **qa/** layer without modifying your ingestion outputs.

```
repo_root/
  qa_configs/
    qa.thresholds.yaml
    qa.sources.baselines.yaml
    qa.boilerplate.allowlist.txt
    qa.sec.sections.yaml
  qa_scripts/
    qa_schema_validate.py
    qa_metadata_validate.py
    qa_text_quality.py
    qa_chunk_quality.py
    qa_dedupe_audit.py
    qa_boilerplate_mine.py
    qa_link_health_retest.py
    qa_coverage_report.py
    qa_persona_tag_precision.py
    qa_sec_section_validate.py
    qa_eval_seed_validate.py
    qa_ground_truth_builder.py
    qa_verification_gate.py
    qa_regression_pack.py
  qa_data/
    baselines/
      ground_truth_dates.csv
      newsroom_rss_dates.csv
    outputs/
      schema_report.json
      metadata_report.json
      text_quality_report.json
      chunk_quality_report.json
      dedupe_audit.json
      boilerplate_signatures.json
      link_health_retest.json
      coverage_report.json
      persona_tag_precision.json
      sec_section_report.json
      eval_seed_report.json
      verification_gate.json
    samples/
      manual_review_samples/
        docs_for_review.csv
        chunks_for_review.csv
  (existing)
  configs/...           (from your Day‑1)
  scripts/...           (from your Day‑1)
  data/raw/...
  data/interim/normalized/*.json
  data/interim/chunks/*.chunks.jsonl
  data/interim/chunks/filtered/*.chunks.jsonl
  data/interim/dedup/dedup_map.json
  data/final/inventory/salesforce_inventory.csv
  data/final/reports/day1_verification.json
```

**Conventions**

*   QA scripts mirror your main pipeline: each writes a JSON report to `qa_data/outputs/` and (when applicable) CSV samples to `qa_data/samples/`.
*   All QA scripts support `--input-glob`, `--limit`, `--fail-on`, and `--out` flags and log to `logs/qa/<script_name>/YYYYMMDD_HHMMSS.log`.

* * *

2) Inputs Under Test (IUT)
--------------------------

*   **Normalized docs:** `data/interim/normalized/*.json`
*   **Chunk files (raw & filtered):** `data/interim/chunks/*.chunks.jsonl`, `data/interim/chunks/filtered/*.chunks.jsonl`
*   **Dedup map:** `data/interim/dedup/dedup_map.json`
*   **Inventory:** `data/final/inventory/salesforce_inventory.csv`
*   **Link health:** `data/final/reports/link_health.json`
*   **Eval seed:** `data/interim/eval/salesforce_eval_seed.jsonl`
*   **Raw sources** (for cross‑validation): `data/raw/**` (HTML/PDF/meta.json)

* * *

3) QA Tests (Scripts, Roles, Inputs, Outputs, Metrics)
------------------------------------------------------

### 3.1 Schema & Field Validation

**Script:** `qa_schema_validate.py`  
**Purpose:** Ensure every normalized doc conforms to the **frozen metadata dictionary**.

*   **Inputs:** `data/interim/normalized/*.json`, `configs/metadata.dictionary.yaml`
*   **Checks:**
    *   Required fields present: `doc_id, company, doctype, title, publish_date, url, source_domain, section, topic, persona_tags, language, text, word_count, token_count, ingestion_ts, hash_sha256`.
    *   Types & enums respected (`doctype`, `language='en'`, `source_domain` in allowed set).
    *   Non‑empty constraints (`title`, `text`, `url`).
    *   `publish_date` ISO‑8601 format.
*   **Outputs:** `qa_data/outputs/schema_report.json` with:
    *   `total_docs`, `docs_valid`, `missing_fields_breakdown`, `enum_violations`, `type_violations`, `examples` (up to 20).
*   **Pass/Fail:** **≥ 98%** valid; else **fail**.

### 3.2 Metadata Correctness & Date Cross‑Validation

**Script:** `qa_metadata_validate.py`  
**Purpose:** Verify **date/title/url** against **independent** baselines to catch extraction mistakes.

*   **Inputs:**
    *   Normalized docs, raw pages (`data/raw/**`), `qa_configs/qa.sources.baselines.yaml`.
    *   Build ground truth via `qa_ground_truth_builder.py` (below).
*   **Cross‑checks by source type:**
    *   **SEC:** parse “Filed” date from raw HTML/PDF headers or EDGAR index page; must equal `publish_date`.
    *   **Investor/Newsroom:** compare `publish_date` to RSS `pubDate` or visible dateline if available.
    *   **Product/Dev/Help:** compare to HTTP `Last-Modified` (±3 days tolerance) if no on‑page date.
    *   **Wikipedia:** compare to page “last modified” (same day or ±1 day).
*   **Outputs:** `qa_data/outputs/metadata_report.json` with field‑level diffs.
*   **Pass/Fail:** **Date match rate ≥ 97%**, **Title match rate ≥ 98%**, `final_url` domain within allowlist **100%**.

**Builder:** `qa_ground_truth_builder.py`

*   **Role:** From raw artifacts and auxiliary feeds, write:
    *   `qa_data/baselines/ground_truth_dates.csv` → `doc_id, source_type, baseline_date, baseline_title, baseline_url, method`
    *   `qa_data/baselines/newsroom_rss_dates.csv` → feed URL, item URL, pubDate.

### 3.3 Text Quality & Garble Detection

**Script:** `qa_text_quality.py`  
**Purpose:** Detect garbled text, encoding issues, and extraction noise.

*   **Inputs:** normalized docs and chunk files.
*   **Checks & metrics:**
    *   **Printable ratio** per doc and per chunk ≥ **0.995** (printable chars / total).
    *   **Replacement char** (`�`) count = 0 for **≥ 99%** docs.
    *   **Language prob. (en)** ≥ **0.9** per doc.
    *   **Stopword ratio** within **\[0.25, 0.65\]** for English prose.
    *   **Character bigram entropy** within **\[2.5, 5.0\]** bits/char (too low = repetition; too high = binary noise).
    *   **Title echo suppression:** first 300 chars of doc should not be **\> 40%** identical to page chrome (use boilerplate signatures from §3.5).
*   **Outputs:** `qa_data/outputs/text_quality_report.json` summarizing violations, with CSV samples for manual review in `qa_data/samples/manual_review_samples/`.

### 3.4 Chunk Quality & Boundary Integrity

**Script:** `qa_chunk_quality.py`  
**Purpose:** Validate chunk sizes, overlaps, and section boundaries.

*   **Inputs:** chunk files (raw & filtered), normalized docs, `configs/chunking.config.json`.
*   **Checks:**
    *   **Length:** median tokens per chunk in **\[650, 950\]**; **≥ 90%** chunks within **\[500, 1100\]**; short‑doc rule respected.
    *   **Overlap:** consecutive chunks per doc share **\[80, 160\]** tokens on average; **no negative overlaps**.
    *   **SEC boundary rule:** **0** chunks cross an `Item` boundary.
    *   **Heading continuity:** `local_heads[]` present for **≥ 95%** of chunks.
*   **Outputs:** `qa_data/outputs/chunk_quality_report.json`.

### 3.5 Boilerplate Mining & Signature List

**Script:** `qa_boilerplate_mine.py`  
**Purpose:** Explain high duplicate rate; learn a **boilerplate signature list** to filter recurring footers/CTAs.

*   **Inputs:** chunk text across all PR/product pages.
*   **Method:**
    *   Extract top **n‑grams (n=8..20)** with **doc frequency ≥ 8** and **span length ≥ 150 chars**.
    *   Cluster near‑identical n‑grams; output signatures with `source_domain` and average span.
    *   Label as candidate boilerplate if appears in **≥ 10 docs** with **≥ 0.85** Jaccard against spans.
*   **Outputs:**
    *   `qa_data/outputs/boilerplate_signatures.json` (ranked list).
    *   Update file: `qa_configs/qa.boilerplate.allowlist.txt` (approved signatures to filter in normalization).
*   **Acceptance:** ability to explain **≥ 80%** of duplicate spans by boilerplate presence.

### 3.6 Dedupe Audit & Parameter Grid

**Script:** `qa_dedupe_audit.py`  
**Purpose:** Quantify duplicates by cause and test alternative thresholds non‑destructively.

*   **Inputs:** original chunks, `data/interim/dedup/dedup_map.json`, boilerplate signatures.
*   **Analyses:**
    *   **By doctype/domain**: duplicate share; top offending templates.
    *   **Cause attribution**: proportion due to boilerplate vs actual content repetition.
    *   **Grid search**: Jaccard thresholds **{0.85, 0.90, 0.95}** × shingle sizes **{5, 7}** × “ignore boilerplate” **{on, off}**; compute resulting duplicate ratios & retained unique chunks.
*   **Outputs:** `qa_data/outputs/dedupe_audit.json` with a recommended setting (must bring **post‑filter duplicate ≤ 15%**).
*   **Remediation decision rule:**
    1.  Apply boilerplate filter in normalization;
    2.  Re‑run dedupe at **0.90/5**;
    3.  Only if still > 15%, consider **0.95/5**.

### 3.7 Link Health Re‑Test (Stability)

**Script:** `qa_link_health_retest.py`  
**Purpose:** Confirm **100%** link health persists; detect domain drift.

*   **Inputs:** `data/final/reports/link_health.json`, normalized docs.
*   **Checks:**
    *   Re‑request **10%** random sample plus **all** previously failing or redirected URLs.
    *   Verify `final_url` domain ∈ {`sec.gov`, `investor.salesforce.com`, `salesforce.com`, `developer.salesforce.com`, `help.salesforce.com`, `wikipedia.org`}.
*   **Outputs:** `qa_data/outputs/link_health_retest.json`.
*   **Pass/Fail:** 100% success; else flag docs for refresh.

### 3.8 Coverage & Recency Report

**Script:** `qa_coverage_report.py`  
**Purpose:** Ensure the corpus is balanced and recent.

*   **Inputs:** inventory CSV + normalized docs.
*   **Metrics:**
    *   Counts by `doctype` & `source_domain`.
    *   PR within last 12 months (≥ 8).
    *   SEC presence: at least 1 each of 10‑K, 10‑Q, 8‑K.
    *   Date distribution histograms (month buckets).
*   **Outputs:** `qa_data/outputs/coverage_report.json`.

### 3.9 Persona Tag Precision (Heuristic Audit)

**Script:** `qa_persona_tag_precision.py`  
**Purpose:** Validate that `persona_tags` make sense.

*   **Inputs:** normalized docs, `configs/eval.prompts.yaml`.
*   **Method:** For each doc with non‑empty `persona_tags`, verify **≥ 1** persona keyword appears in `text`.
*   **Outputs:** `qa_data/outputs/persona_tag_precision.json` with per‑persona precision.
*   **Pass/Fail:** precision **≥ 0.80** for each persona; else review lexicon.

### 3.10 SEC Section Validation

**Script:** `qa_sec_section_validate.py`  
**Purpose:** Confirm **Item boundaries** are found and in order.

*   **Inputs:** normalized SEC docs + section span map (from your SEC parser).
*   **Checks:** presence and **order** of `Item 1`, `Item 1A`, `Item 7`, `Item 7A`, `Item 8`; **no crossing** spans.
*   **Outputs:** `qa_data/outputs/sec_section_report.json`.
*   **Pass/Fail:** 100% of SEC docs satisfy these checks.

### 3.11 Eval Seed Integrity

**Script:** `qa_eval_seed_validate.py`  
**Purpose:** Ensure the evaluation dataset is **usable and correct**.

*   **Inputs:** `data/interim/eval/salesforce_eval_seed.jsonl`, chunks.
*   **Checks:**
    *   Each `expected_chunk_id` exists and `doc_id` matches.
    *   All `expected_answer_keyphrases[]` found in that chunk’s text.
    *   Balanced coverage: per persona (≥ 10 each) and per source type (SEC ≥ 10, PR ≥ 10, product/docs/help ≥ 8, wiki ≥ 2).
*   **Outputs:** `qa_data/outputs/eval_seed_report.json`.
*   **Pass/Fail:** all keyphrases present for **100%** of records; balance satisfied.

### 3.12 Gate Aggregation & Sign‑off

**Script:** `qa_verification_gate.py`  
**Purpose:** Aggregate all QA reports; enforce pass criteria; output a single **go/no‑go** JSON.

*   **Inputs:** all `qa_data/outputs/*.json`
*   **Output:** `qa_data/outputs/verification_gate.json` with:
    *   `status: PASS|FAIL`,
    *   `failed_checks[]` (id, summary, blocking vs advisory),
    *   `remediation_actions[]` (ordered list pointing to §8).

### 3.13 Regression Pack (Optional but Recommended)

**Script:** `qa_regression_pack.py`  
**Purpose:** After any remediation (e.g., normalization change), re‑run a **fixed subset** of QA tests to detect regressions.

*   **Inputs:** list of critical checks from `qa.thresholds.yaml`.
*   **Output:** `qa_data/outputs/regression_pack.json` (diff vs previous run).

* * *

4) QA Thresholds (freeze in `qa_configs/qa.thresholds.yaml`)
------------------------------------------------------------

*   **Schema valid docs:** ≥ 98%
*   **Date match rate:** ≥ 97%
*   **Title match rate:** ≥ 98%
*   **Link health:** 100%
*   **Duplicate rate (post‑boilerplate):** ≤ 15%
*   **Exact duplicate docs:** ≤ 5%
*   **Printable ratio:** ≥ 0.995
*   **Replacement char free docs:** ≥ 99%
*   **Language prob. (en):** ≥ 0.9
*   **Stopword ratio:** \[0.25, 0.65\]
*   **Entropy:** \[2.5, 5.0\] bits/char
*   **Chunk length coverage:** ≥ 90% within \[500, 1100\] tokens
*   **Overlap window:** mean in \[80, 160\]
*   **SEC section pass:** 100%
*   **Persona tag precision:** ≥ 0.80
*   **Eval seed integrity:** 100% keys present; distribution balanced

* * *

5) Ground‑Truth Construction (independent baselines)
----------------------------------------------------

**Script:** `qa_ground_truth_builder.py` (run first)

*   **SEC:** parse “Filed” date and title from raw EDGAR HTML/PDF; if available, also parse from EDGAR index meta.json created by your fetcher.
*   **Newsroom/Investor:** for RSS‑sourced items, use `pubDate` as baseline; for IR pages, use dateline text; store both.
*   **Product/Docs/Help:** use HTTP `Last-Modified` header (fall back to parsed “Updated” text).
*   **Wikipedia:** parse “last modified” banner or HTTP header.

**Outputs:**

*   `qa_data/baselines/ground_truth_dates.csv` (`doc_id, baseline_date, baseline_title, baseline_url, method`)
*   `qa_data/baselines/newsroom_rss_dates.csv` (for cross‑checking PR dates)

* * *

6) Manual Review Samples (for spot checks)
------------------------------------------

Generate **audit samples** for human review (these do not block QA automation but guide fixes):

*   `qa_data/samples/manual_review_samples/docs_for_review.csv`
    *   5 random docs per doctype, plus any failing docs.
    *   Columns: `doc_id, doctype, title, publish_date, url, flags(schema|metadata|text|link|sec_section)`.
*   `qa_data/samples/manual_review_samples/chunks_for_review.csv`
    *   5 random chunks per doctype + failing examples; include `text[:400]`, `local_heads`, `overlap_prev`, `overlap_next`, `dup_status`.

**Checklist for reviewer:**

*   Title accurate? Date matches page? Text readable? Any residual boilerplate? Chunk boundaries logical? Claims traceable?

* * *

7) Execution Order (Runbook)
----------------------------

1.  `qa_ground_truth_builder.py`
2.  `qa_schema_validate.py`
3.  `qa_metadata_validate.py`
4.  `qa_text_quality.py`
5.  `qa_chunk_quality.py`
6.  `qa_boilerplate_mine.py`
7.  `qa_dedupe_audit.py`
8.  `qa_link_health_retest.py`
9.  `qa_coverage_report.py`
10.  `qa_persona_tag_precision.py`
11.  `qa_sec_section_validate.py`
12.  `qa_eval_seed_validate.py`
13.  `qa_verification_gate.py` (aggregates; PASS/FAIL)
14.  If FAIL → apply **remediation actions** (§8) → re‑run `qa_regression_pack.py` + `qa_verification_gate.py`.

* * *

8) Remediation Actions (ordered, with outputs)
----------------------------------------------

> You reported **dedupe > 15%** (21%). Run these **in order** and capture the artifacts:

1.  **Boilerplate removal:**
    *   Use `qa_boilerplate_mine.py` signatures to extend `configs/normalization.rules.yaml` and `qa_configs/qa.boilerplate.allowlist.txt` (document selectors or text snippets to strip).
    *   **Artifact:** `qa_data/outputs/boilerplate_signatures.json` + rules diff.
2.  **Normalization re‑run (targeted):**
    *   Re‑normalize only PR/product pages affected (use `--doctype press,product`).
    *   Re‑chunk those docs only.
3.  **Re‑dedupe at 0.90/5:**
    *   Rebuild `data/interim/dedup/dedup_map.json` on affected chunks.
    *   **Expected outcome:** duplicate ≤ 15%. If not…
4.  **Tighten to 0.95/5 (last resort):**
    *   Only if boilerplate‑filtered duplicate remains > 15%.
    *   Record **before/after** unique chunk counts and report in `qa_data/outputs/dedupe_audit.json`.
5.  **Text fixes (if garbled):**
    *   If `qa_text_quality.py` flags garble, add source‑specific extraction rules (e.g., remove hidden nodes, decode entities).
    *   Re‑normalize → re‑chunk affected docs.
6.  **Date fixes:**
    *   If `qa_metadata_validate.py` flags mismatches, adjust `extract_metadata.py` precedence rules (do not override SEC “Filed” dates).
    *   Re‑extract metadata for failing docs only.
7.  **Persona lexicon tuning:**
    *   If precision < 0.80, adjust keyword lists in `configs/eval.prompts.yaml`; re‑compute `persona_tags` for only affected docs.
8.  **Re‑QA:**
    *   Run `qa_regression_pack.py` + `qa_verification_gate.py`.
    *   **Artifact:** `qa_data/outputs/regression_pack.json` + updated `verification_gate.json`.

* * *

9) Deliverables (QA Sprint)
---------------------------

*   `qa_configs/qa.thresholds.yaml` (frozen thresholds)
*   `qa_configs/qa.sources.baselines.yaml` (baseline methods per source)
*   `qa_configs/qa.boilerplate.allowlist.txt` (approved boilerplate patterns)
*   `qa_configs/qa.sec.sections.yaml` (SEC item expectations)
*   `qa_data/baselines/ground_truth_dates.csv`, `newsroom_rss_dates.csv`
*   `qa_data/outputs/*.json` reports (one per test)
*   `qa_data/samples/manual_review_samples/*.csv` (spot‑check packs)
*   `qa_data/outputs/verification_gate.json` (final PASS/FAIL)
*   **Change diffs** to:
    *   `configs/normalization.rules.yaml` (if updated)
    *   `configs/metadata.dictionary.yaml` (if schema clarifications are needed; avoid changes unless strictly required)
    *   `data/interim/*` & `data/final/*` (updated artifacts as a result of remediation)

* * *

10) Evaluation Dataset (Integrity‑First)
----------------------------------------

You already generated **≥ 40** eval pairs. This QA adds **consistency controls**:

*   `qa_eval_seed_validate.py` ensures every pair is **addressable** (chunk exists) and **contentful** (keyphrases present).
*   If any pair fails, the script should:
    *   Flag it and **auto‑replace** with a new pair from the same source type & persona, or
    *   Move it to a `rejected` partition with reasons.

**Pass criteria:** 100% pairs valid; per‑persona ≥ 10; per‑doctype distribution met (SEC ≥ 10, PR ≥ 10, product/docs/help ≥ 8, wiki ≥ 2).

* * *

11) One‑Day QA Sprint Timeline & Milestones
-------------------------------------------

> This is a focused post‑ingestion QA sprint. Adjust if remediation is needed.

**AM (2–3 hours)**

1.  Build ground truths → Run schema, metadata, text, chunk tests → Generate coverage & section reports.
    *   **Milestones:** reports written; top issues identified.

**Midday (1–2 hours)**  
2) Boilerplate mining → Dedupe grid audit.

*   **Milestones:** recommended boilerplate signatures + dedupe parameters.

**PM (2–3 hours)**  
3) Apply remediation (update normalization rules; target re‑normalize PR/product) → Re‑dedupe → Re‑run regression pack + gate.

*   **Milestones:** **verification\_gate.json = PASS** and duplicate ≤ 15%.

* * *

12) What this catches beyond duplicates
---------------------------------------

*   **Incorrect extraction:** date/title mismatches vs independent baselines; URL canonicalization errors.
*   **Garbled text:** encoding artifacts, unprintable chars, wrong order (entropy & replacement char checks).
*   **Sectioning errors:** SEC item boundaries crossing.
*   **Chunking pathologies:** too short/long chunks, missing overlaps, lost headings.
*   **Persona label noise:** mismatch between tags and content.
*   **Coverage drift:** missing SEC or recency imbalance.
*   **Link drift:** domains or redirects that later break.

* * *

13) Acceptance Summary (what “PASS” means)
------------------------------------------

*   `qa_data/outputs/verification_gate.json` shows **PASS** and **no critical failed checks**.
*   `qa_data/outputs/dedupe_audit.json` shows **post‑boilerplate duplicate ≤ 15%** (and explains causes).
*   All other reports within thresholds, with remediation diffs recorded.

* * *

### Notes tailored to your current status

*   Your **duplicate rate (21%)** is very likely due to **newsroom/press footers & CTAs** replicated across many pages. Run **§3.5 Boilerplate Mining** then **§3.6 Dedupe Audit**. In most corpora, enabling boilerplate stripping and raising the dedupe threshold from **0.85 → 0.90** is sufficient.
*   Because you already have **100% link health** and **97 docs with valid dates**, the highest ROI is in **boilerplate filtering** + **SEC section & text quality checks** to prevent subtle errors before indexing.

This blueprint gives the implementation model everything needed to build a **comprehensive, repeatable QA harness**, pinpoint issues (including your duplicate‑rate overage), and produce clear, auditable evidence that your Day‑1 dataset **meets spec**.

## Prompt:
below is my coding result, how I fully test my data? and give me two answers, 1. is all the test method that available to me and why I need to run that.
2. is a quick test, that are important to run before my next step
"""
i’ve added a complete QA layer matching your blueprint. It’s structured, configurable, and outputs JSON reports plus sample CSVs for manual review.

What I Added

qa_configs

qa.thresholds.yaml: frozen acceptance thresholds.
qa.sources.baselines.yaml: per‑source baseline methods and domain allowlist.
qa.boilerplate.allowlist.txt: seed list for safe-to-strip signatures.
qa.sec.sections.yaml: required SEC items list.
qa_scripts

qa_ground_truth_builder.py: builds baselines from data/raw/** into CSVs.
qa_schema_validate.py: validates normalized docs against configs/metadata.dictionary.yaml.
qa_metadata_validate.py: compares dates/titles/URLs vs baselines and domain allowlist.
qa_text_quality.py: printable ratio, replacement char, stopword ratio, bigram entropy.
qa_chunk_quality.py: chunk length distribution, overlap estimate, SEC boundary crossing, heads presence.
qa_boilerplate_mine.py: mines recurring n‑gram spans; writes signatures and updates allowlist.
qa_dedupe_audit.py: duplicate attribution and grid search (thresholds × shingles), with recommendation.
qa_link_health_retest.py: 10% sample + prior failures; rechecks GET/HEAD with domain validation.
qa_coverage_report.py: doctype/domain counts, month histogram, PR recency, SEC presence.
qa_persona_tag_precision.py: checks persona tag precision vs keyword lexicon.
qa_sec_section_validate.py: verifies Items 1, 1A, 7, 7A, 8 presence and order.
qa_eval_seed_validate.py: ensures chunk exists and keyphrases appear; reports persona/source balance.
qa_verification_gate.py: aggregates all QA outputs into a PASS/FAIL decision.
qa_regression_pack.py: compares current vs previous critical QA reports.
qa_manual_samples.py: emits docs_for_review.csv and chunks_for_review.csv with flagged examples.
qa_scripts/_qa_common.py

Shared QA helpers (logger to logs/qa/<script>/..., token/overlap utils, entropy, etc.) and import bridge to scripts/_common.py.
Outputs

Reports under qa_data/outputs/:
schema_report.json, metadata_report.json, text_quality_report.json, chunk_quality_report.json, boilerplate_signatures.json, dedupe_audit.json, link_health_retest.json, coverage_report.json, persona_tag_precision.json, sec_section_report.json, eval_seed_report.json, verification_gate.json, regression_pack.json
Baselines under qa_data/baselines/:
ground_truth_dates.csv, newsroom_rss_dates.csv
Samples under qa_data/samples/manual_review_samples/:
docs_for_review.csv, chunks_for_review.csv
Runbook (Order)

python qa_scripts/qa_ground_truth_builder.py
python qa_scripts/qa_schema_validate.py
python qa_scripts/qa_metadata_validate.py
python qa_scripts/qa_text_quality.py
python qa_scripts/qa_chunk_quality.py
python qa_scripts/qa_boilerplate_mine.py
python qa_scripts/qa_dedupe_audit.py
python qa_scripts/qa_link_health_retest.py
python qa_scripts/qa_coverage_report.py
python qa_scripts/qa_persona_tag_precision.py
python qa_scripts/qa_sec_section_validate.py
python qa_scripts/qa_eval_seed_validate.py
python qa_scripts/qa_verification_gate.py
Optional: python qa_scripts/qa_manual_samples.py and python qa_scripts/qa_regression_pack.py
All QA scripts support common flags like --input-glob/--limit/--out (where applicable) and log to logs/qa/<script>/....

Notes / Known Gaps (visible in QA)

Domain enum vs current source_domain: your normalized docs collapse subdomains (e.g., developer.salesforce.com → salesforce.com). The schema validator and metadata domain checks will flag this. If desired, I can add subdomain preservation or relax schema.
Publish date precedence: existing extractor prefers the doc’s embedded date (from doc_id) over baselines when missing; QA will expose mismatches. I can patch scripts/extract_metadata.py to prefer backfilled baselines.
Chunk heads: current chunker doesn’t populate local_heads[]. QA will mark low heads coverage; we can add heading capture in normalization and propagate into chunks.
Title echo suppression, language probability: QA includes core text checks (printable/entropy/stopwords). If you want title echo and calibrated lang probability, I can extend qa_text_quality.py to use a lightweight heuristic or optional dependency.
"""

## Response:
Thought for 33s

We need to break this into two parts: first, listing all the test methods with reasons why they’re necessary — these maps to risks and acceptance thresholds. Then, we should give a quick subset of tests to run before the next step. No code, just actionable steps, commands, order, pass/fail criteria, and interpretation. We'll skip external references since it's internal dataset QA. Let's also remember to follow the QA layer, addressing known gaps (like domain enums or missing chunk heads).

We need to organize and restate their existing thresholds, linking them to each test and explaining the rationale behind possible failure scenarios. The structure will include:

*   Risk mapping to tests.
*   Details for each test script (inputs, thresholds, failure signs).
*   "Triage matrix" to decide whether to proceed or fix.
*   Artifact contract tests (e.g., document integrity).
*   Sampling review guidelines.
*   Regression pack gating.
*   Ensure to provide system-friendly time/cost estimates and explain verification\_gate.json.

For quick remediation before the next step, we'll focus on a minimal set of tests to catch showstoppers: schema validation, metadata validity, text quality checks, chunk boundaries, deduplication under 15%, link health, and SEC section presence. I’ll ensure to keep things clear, with step-by-step CLI commands and specifics on pass/fail criteria. I'll organize into two parts: comprehensive testing methods and a fast, essential test path, using a “stoplight dashboard” and “verification\_gate”.

I need to create structured lists, using bullet points to keep the details comprehensive without being overly verbose. The user asked for thorough answers and to list all available tests and their reasons. I’ll avoid redundancy, exclude chain-of-thought, and make sure everything is clear, succinct, and respects requirements.

Done

awesome — since you already wired up the QA layer, here are the two things you asked for:

1) Full test catalog you can (and should) run — what each test proves & why it matters
======================================================================================

Below maps every QA script you have to the exact risk it mitigates, what it reads/writes, the pass thresholds, and what to do if it fails. This is the “run everything” checklist before you ship the dataset to indexing.

**Legend (Blocking vs Advisory)**

*   **BLOCKING** = must pass before the next stage (indexing/router/evals)
*   **ADVISORY** = good hygiene; fix soon, but doesn’t block staged runs

* * *

### A. Ground truth baselines (prepare once)

**Script:** `qa_scripts/qa_ground_truth_builder.py`  
**Reads:** `data/raw/**` (HTML/PDF + `.meta.json`)  
**Writes:** `qa_data/baselines/ground_truth_dates.csv`, `qa_data/baselines/newsroom_rss_dates.csv`  
**Why:** Builds independent dates/titles/URLs so later tests can catch extraction mistakes.  
**Gate:** N/A (prereq) — **BLOCKING** for the rest of QA.

* * *

### B. Schema conformance (no missing fields or wrong enums)

**Script:** `qa_scripts/qa_schema_validate.py`  
**Reads:** `data/interim/normalized/*.json`, `configs/metadata.dictionary.yaml`  
**Writes:** `qa_data/outputs/schema_report.json`  
**Checks:** required fields, types, enums (`doctype`, `source_domain`), ISO date format  
**Pass:** ≥ **98%** docs valid  
**Why:** Catches structural defects that would crash indexers and tools.  
**If fail:** Fix extractor/normalizer; re-run.  
**Severity:** **BLOCKING**

* * *

### C. Metadata correctness (dates/titles/URLs really match the source)

**Script:** `qa_scripts/qa_metadata_validate.py` (uses baselines from A)  
**Reads:** normalized docs + baselines CSVs  
**Writes:** `qa_data/outputs/metadata_report.json`  
**Checks:**

*   SEC “Filed” date equals `publish_date`
*   PR/blog date equals RSS/dateline
*   Product/dev/help date equals “Updated” or HTTP `Last-Modified` (±3d)
*   Domain allowlist respected  
    **Pass:** Date match ≥ **97%**; title match ≥ **98%**; domains 100% in allowlist  
    **Why:** Prevents incorrect timestamps (a top cause of stale or misranked insights).  
    **If fail:** Adjust `scripts/extract_metadata.py` precedence; re-extract for offenders only.  
    **Severity:** **BLOCKING**

* * *

### D. Text quality & garble detection

**Script:** `qa_scripts/qa_text_quality.py`  
**Reads:** normalized docs, chunk files  
**Writes:** `qa_data/outputs/text_quality_report.json`, sample CSVs for review  
**Checks:** printable ratio ≥ **0.995**; replacement char (`�`) absent in ≥ **99%** docs; English prob ≥ **0.9**; stopword ratio \[0.25, 0.65\]; char-bigram entropy \[2.5, 5.0\]  
**Why:** Guards against HTML extraction glitches, PDF OCR noise, double-encoding.  
**If fail:** Tighten normalizer (strip hidden nodes, decode entities) and re-normalize only flagged docs.  
**Severity:** **BLOCKING** (garbled text poisons embeddings)

* * *

### E. Chunk integrity (sizes, overlaps, headings, SEC boundaries)

**Script:** `qa_scripts/qa_chunk_quality.py`  
**Reads:** chunk files (raw & filtered), normalized docs, `configs/chunking.config.json`  
**Writes:** `qa_data/outputs/chunk_quality_report.json`  
**Checks:**

*   90% of chunks in \[500, 1100\] tokens; median in \[650, 950\]
*   Average overlap in \[80, 160\] tokens; no negative overlaps
*   `local_heads[]` present in ≥ **95%** chunks
*   **SEC rule:** 0 chunks cross `Item 1|1A|7|7A|8` boundaries  
    **Why:** Ensures retrieval fidelity and consistent context windows.  
    **If fail:** Fix chunker parameters; propagate headings from normalization; re-chunk affected docs.  
    **Severity:** **BLOCKING**

* * *

### F. Boilerplate mining (find repeat footers/CTAs that inflate duplicates)

**Script:** `qa_scripts/qa_boilerplate_mine.py`  
**Reads:** chunk text across PR/product/blog  
**Writes:** `qa_data/outputs/boilerplate_signatures.json`, updates `qa_configs/qa.boilerplate.allowlist.txt`  
**Checks:** n-gram spans (8–20) with doc frequency ≥ 10 and Jaccard ≥ 0.85  
**Why:** Your duplicate rate (21%) is almost always template boilerplate; mining gives surgical removal rules.  
**If fail:** N/A; this is discovery.  
**Severity:** **ADVISORY** alone, but **prereq** to the dedupe fix next.

* * *

### G. Dedupe attribution & parameter grid (prove ≤ 15% duplicates post-filter)

**Script:** `qa_scripts/qa_dedupe_audit.py`  
**Reads:** raw chunks, filtered chunks, `data/interim/dedup/dedup_map.json`, boilerplate signatures  
**Writes:** `qa_data/outputs/dedupe_audit.json`  
**Checks:**

*   Duplicate share by doctype/domain
*   Attribution (boilerplate vs real repetition)
*   Grid: thresholds {0.85, 0.90, 0.95} × shingle {5,7} × ignore-boilerplate {on,off}  
    **Pass:** Recommended setting yields **≤ 15%** dupes without excessive content loss  
    **Why:** Quantifies and fixes the exact issue you observed.  
    **If fail:** Apply mined boilerplate filters; re-normalize PR/product only; re-run dedupe at 0.90/5; only then consider 0.95/5.  
    **Severity:** **BLOCKING**

* * *

### H. Link health stability (retest)

**Script:** `qa_scripts/qa_link_health_retest.py`  
**Reads:** `data/final/reports/link_health.json`, normalized docs  
**Writes:** `qa_data/outputs/link_health_retest.json`  
**Checks:** recheck 10% sample + all prior redirects/fails; verify final domains in allowlist  
**Pass:** 100% OK  
**Why:** Links rot quickly; verify your 100% still holds.  
**If fail:** Refresh those docs; update `final_url`.  
**Severity:** **BLOCKING**

* * *

### I. Coverage & recency shape

**Script:** `qa_scripts/qa_coverage_report.py`  
**Reads:** inventory CSV + normalized docs  
**Writes:** `qa_data/outputs/coverage_report.json`  
**Checks:** counts by `doctype`/domain; PR last 12 months ≥ 8; SEC presence: ≥1 10-K, ≥1 10-Q, ≥1 8-K  
**Why:** Prevents skew (e.g., only PR, no filings).  
**If fail:** Fetch a missing filing or swap stale PRs for recent ones.  
**Severity:** **BLOCKING**

* * *

### J. Persona tag precision (heuristic)

**Script:** `qa_scripts/qa_persona_tag_precision.py`  
**Reads:** normalized docs, `configs/eval.prompts.yaml`  
**Writes:** `qa_data/outputs/persona_tag_precision.json`  
**Checks:** precision ≥ **0.80** that persona keywords actually occur in doc text  
**Why:** Avoids misleading routing later (persona-aware prompts).  
**If fail:** Tweak lexicon; re-tag only offenders.  
**Severity:** **ADVISORY** (nice to have, won’t break indexing)

* * *

### K. SEC section detection

**Script:** `qa_scripts/qa_sec_section_validate.py`  
**Reads:** normalized SEC docs + section spans  
**Writes:** `qa_data/outputs/sec_section_report.json`  
**Checks:** presence and order of Items 1, 1A, 7, 7A, 8; no span crossings  
**Why:** Guarantees filings are structurally reliable for section-specific retrieval.  
**If fail:** Improve regex anchors; re-normalize SEC docs.  
**Severity:** **BLOCKING**

* * *

### L. Eval seed integrity (retrieval-readiness)

**Script:** `qa_scripts/qa_eval_seed_validate.py`  
**Reads:** `data/interim/eval/salesforce_eval_seed.jsonl`, chunks  
**Writes:** `qa_data/outputs/eval_seed_report.json`  
**Checks:** every `expected_chunk_id` exists; all keyphrases present; balanced distribution (SEC ≥ 10, PR ≥ 10, product/docs/help ≥ 8, wiki ≥ 2; ≥ 10 per persona)  
**Why:** Ensures tomorrow’s retrieval metrics are meaningful.  
**If fail:** Auto-replace failing pairs from same source type; regenerate balance.  
**Severity:** **BLOCKING**

* * *

### M. Gate aggregation (single decision)

**Script:** `qa_scripts/qa_verification_gate.py`  
**Reads:** all `qa_data/outputs/*.json`  
**Writes:** `qa_data/outputs/verification_gate.json` with PASS/FAIL and blocking reasons  
**Why:** One-button confidence to proceed.  
**Severity:** **BLOCKING**

* * *

### N. Regression pack (after any fix)

**Script:** `qa_scripts/qa_regression_pack.py`  
**Reads:** previous vs current QA outputs  
**Writes:** `qa_data/outputs/regression_pack.json`  
**Why:** Ensures a fix (e.g., new boilerplate rules) didn’t regress dates/links/sections.  
**Severity:** **ADVISORY**, but strongly recommended after any remediation

* * *

What specifically addresses your noted issues
---------------------------------------------

*   **Duplicate rate > 15%** → Run **F → G** (mine boilerplate, then dedupe grid), apply allowlist rules, re-normalize **press/product only**, re-dedupe at **0.90/5**, re-gate.
*   **Potential incorrect extraction / garbled text** → **C + D** catch date/title/url mismatches and encoding/garble; pair with **E** for chunk boundary correctness.

* * *

2) “Quick test” you should run **before** the next step (fast go/no-go)
=======================================================================

Run this minimal set in order; it catches the top showstoppers with the least runtime. If all green, you can safely proceed to indexing and router work while you polish advisory items in parallel.

**Quick sequence & pass gates**

1.  **Baselines:**
    *   `python qa_scripts/qa_ground_truth_builder.py`
    *   _Reason:_ prerequisite for metadata checks.
2.  **Schema & metadata sanity:**
    *   `python qa_scripts/qa_schema_validate.py` → **≥ 98% valid**
    *   `python qa_scripts/qa_metadata_validate.py` → **date ≥ 97%**, **title ≥ 98%**, **domains 100%**
    *   _Reason:_ guarantees structure and timestamps won’t poison ranking.
3.  **Text & chunks (fast blockers):**
    *   `python qa_scripts/qa_text_quality.py` → printable ≥ **0.995**, `�`\-free ≥ **99%**
    *   `python qa_scripts/qa_chunk_quality.py` → size/overlap in range; **0** SEC boundary crossings
    *   _Reason:_ ensures clean embeddings and safe sectioning.
4.  **Duplicates (your current red flag):**
    *   `python qa_scripts/qa_boilerplate_mine.py` (discover)
    *   `python qa_scripts/qa_dedupe_audit.py` → **≤ 15%** using recommended settings (prefer: boilerplate filtered + **0.90/5**)
    *   If still > 15%: apply allowlist, re-normalize **press/product** only, re-run dedupe audit.
    *   _Reason:_ prevents over-pruning or ballooning indexes.
5.  **Coverage + eval readiness:**
    *   `python qa_scripts/qa_coverage_report.py` → PR last 12 mo ≥ **8**; SEC has 10-K + 10-Q + 8-K
    *   `python qa_scripts/qa_eval_seed_validate.py` → **100% pairs valid**, balanced distribution
    *   _Reason:_ confirms you can run retrieval metrics tomorrow.
6.  **Gate:**
    *   `python qa_scripts/qa_verification_gate.py` → **PASS**
    *   _Reason:_ single decision artifact to attach to the handoff.

**If you only have time to fix one thing before moving on:**  
Address duplicates via **boilerplate mining → normalization allowlist → dedupe at 0.90/5**, then re-run the **gate**. This is the single change most likely to improve retrieval quality and reduce index cost.

* * *

Why these quick tests, specifically
-----------------------------------

*   **Schema+metadata** are the most common silent failure modes that later look like “bad ranking.”
*   **Text & chunks** ensure embeddings won’t be garbage-in.
*   **Duplicates** directly affect cost/latency and evaluation fairness.
*   **Coverage+eval seed** guarantee you can compute Recall/nDCG next without rework.
*   **Gate** makes the decision explicit and auditable.

* * *

If you want, I can also suggest a short “interpretation guide” for each JSON report (what fields to glance first, what ranges indicate trouble), but the two lists above will get you confidently to the next stage.

## Prompt:
中文翻译上面内容，保持格式不变，一字不啦

## Response:
awesome — 既然你已经把 QA 层接好了，下面是你要的两个部分：

1) 你可以（而且应该）运行的完整测试目录 —— 每种测试证明了什么 & 为什么要跑
==========================================

下面把你已有的每个 QA 脚本映射到它缓解的具体风险、读写什么、通过阈值，以及失败后怎么做。这是你在把数据集交给索引阶段之前的“全部运行”清单。

**图例（阻断 vs 建议）**

*   **BLOCKING（阻断）** = 在进入下一阶段（索引/路由/评测）前必须通过
*   **ADVISORY（建议）** = 良好卫生；尽快修，但不阻断分阶段运行

* * *

### A. 基线构建（先准备一次）

**脚本：** `qa_scripts/qa_ground_truth_builder.py`  
**读取：** `data/raw/**`（HTML/PDF + `.meta.json`）  
**写入：** `qa_data/baselines/ground_truth_dates.csv`, `qa_data/baselines/newsroom_rss_dates.csv`  
**为什么：** 构建独立的日期/标题/URL 基线，便于后续测试捕捉抽取错误。  
**关卡：** 无（前置条件）——对其余 QA **BLOCKING**。

* * *

### B. 架构一致性（无缺失字段或错误枚举）

**脚本：** `qa_scripts/qa_schema_validate.py`  
**读取：** `data/interim/normalized/*.json`, `configs/metadata.dictionary.yaml`  
**写入：** `qa_data/outputs/schema_report.json`  
**检查：** 必填字段、类型、枚举（`doctype`、`source_domain`）、ISO 日期格式  
**通过：** 文档有效率 ≥ **98%**  
**为什么：** 捕捉会导致索引器和工具崩溃的结构性缺陷。  
**失败处理：** 修抽取/归一化；重跑。  
**严重性：** **BLOCKING**

* * *

### C. 元数据正确性（日期/标题/URL 真正匹配来源）

**脚本：** `qa_scripts/qa_metadata_validate.py`（使用 A 的基线）  
**读取：** 归一化文档 + 基线 CSV  
**写入：** `qa_data/outputs/metadata_report.json`  
**检查：**

*   SEC “Filed” 日期等于 `publish_date`
*   PR/博客日期等于 RSS/文中日期
*   产品/开发/帮助文档日期等于“Updated”或 HTTP `Last-Modified`（±3 天）
*   域名在 allowlist 内  
    **通过：** 日期匹配率 ≥ **97%**；标题匹配率 ≥ **98%**；域名 100% 在 allowlist  
    **为什么：** 防止时间戳错误（排名陈旧或错误的头号原因）。  
    **失败处理：** 调整 `scripts/extract_metadata.py` 的优先级；仅对问题文档重抽取元数据。  
    **严重性：** **BLOCKING**

* * *

### D. 文本质量与乱码检测

**脚本：** `qa_scripts/qa_text_quality.py`  
**读取：** 归一化文档、分块文件  
**写入：** `qa_data/outputs/text_quality_report.json`，并输出用于人工复核的 CSV 样本  
**检查：** 文本可打印比例 ≥ **0.995**；替换字符（`�`）在 ≥ **99%** 文档中为 0；英文概率 ≥ **0.9**；停用词比例 \[0.25, 0.65\]；字符二元组熵 \[2.5, 5.0\]  
**为什么：** 防止 HTML 提取错误、PDF OCR 噪声、双重编码。  
**失败处理：** 加强归一化（去隐藏节点、解码实体），仅对被标记文档重归一化。  
**严重性：** **BLOCKING**（乱码会污染向量）

* * *

### E. 分块完整性（长度、重叠、标题、SEC 边界）

**脚本：** `qa_scripts/qa_chunk_quality.py`  
**读取：** 分块文件（原始 & 过滤）、归一化文档、`configs/chunking.config.json`  
**写入：** `qa_data/outputs/chunk_quality_report.json`  
**检查：**

*   90% 的块在 \[500, 1100\] tokens；中位数在 \[650, 950\]
*   平均重叠在 \[80, 160\] tokens；无负重叠
*   `local_heads[]` 在 ≥ **95%** 块中存在
*   **SEC 规则：** 0 个块跨越 `Item 1|1A|7|7A|8` 边界  
    **为什么：** 确保检索保真度与一致的上下文窗口。  
    **失败处理：** 调整分块参数；从归一化流程传递标题；仅对受影响文档重分块。  
    **严重性：** **BLOCKING**

* * *

### F. 模板挖掘（发现增加重复率的页脚/CTA）

**脚本：** `qa_scripts/qa_boilerplate_mine.py`  
**读取：** PR/产品/博客的分块文本  
**写入：** `qa_data/outputs/boilerplate_signatures.json`，并更新 `qa_configs/qa.boilerplate.allowlist.txt`  
**检查：** 文档频率 ≥ 10、Jaccard ≥ 0.85 的 8–20 元长 n-gram 片段  
**为什么：** 你 21% 的重复率几乎一定源于模板；挖掘可用于外科式清除。  
**失败处理：** N/A；该步骤为发现。  
**严重性：** **ADVISORY**，但下一步去重修复的**前置**

* * *

### G. 去重归因与参数网格（证明过滤后 ≤ 15%）

**脚本：** `qa_scripts/qa_dedupe_audit.py`  
**读取：** 原始分块、过滤后分块、`data/interim/dedup/dedup_map.json`、模板签名  
**写入：** `qa_data/outputs/dedupe_audit.json`  
**检查：**

*   按 `doctype`/域名的重复份额
*   原因归因（模板 vs 实际内容重复）
*   网格：阈值 {0.85, 0.90, 0.95} × shingle {5,7} × ignore-boilerplate {on,off}  
    **通过：** 推荐设置在不过度丢失内容下使重复 ≤ **15%**  
    **为什么：** 量化并修复你观察到的核心问题。  
    **失败处理：** 应用挖掘到的模板过滤；仅对 **press/product** 重归一化；以 **0.90/5** 重去重；若仍不达标再考虑 **0.95/5**。  
    **严重性：** **BLOCKING**

* * *

### H. 链接健康稳定性（复测）

**脚本：** `qa_scripts/qa_link_health_retest.py`  
**读取：** `data/final/reports/link_health.json`、归一化文档  
**写入：** `qa_data/outputs/link_health_retest.json`  
**检查：** 重测 10% 随机样本 + 所有曾重定向/失败的 URL；校验最终域名在 allowlist  
**通过：** 100% OK  
**为什么：** 链接容易腐坏；复核你的 100% 是否仍然成立。  
**失败处理：** 刷新这些文档；更新 `final_url`。  
**严重性：** **BLOCKING**

* * *

### I. 覆盖度与新鲜度形状

**脚本：** `qa_scripts/qa_coverage_report.py`  
**读取：** inventory CSV + 归一化文档  
**写入：** `qa_data/outputs/coverage_report.json`  
**检查：** 按 `doctype`/域名计数；近 12 个月 PR ≥ 8；SEC 存在：≥1 个 10-K、≥1 个 10-Q、≥1 个 8-K  
**为什么：** 防止数据偏斜（例如只有 PR，没有招股文件）。  
**失败处理：** 补抓缺失文件或用更近的 PR 替换陈旧项。  
**严重性：** **BLOCKING**

* * *

### J. 画像标签准确率（启发式）

**脚本：** `qa_scripts/qa_persona_tag_precision.py`  
**读取：** 归一化文档、`configs/eval.prompts.yaml`  
**写入：** `qa_data/outputs/persona_tag_precision.json`  
**检查：** 精度 ≥ **0.80**（画像关键词确实出现在文本中）  
**为什么：** 避免后续路由被误导（画像感知提示）。  
**失败处理：** 调整词表；仅对问题文档重打标签。  
**严重性：** **ADVISORY**（不会阻断索引）

* * *

### K. SEC 分节检测

**脚本：** `qa_scripts/qa_sec_section_validate.py`  
**读取：** 归一化 SEC 文档 + 分节跨度  
**写入：** `qa_data/outputs/sec_section_report.json`  
**检查：** `Item 1, 1A, 7, 7A, 8` 的存在与顺序；无跨度交叉  
**为什么：** 确保申报文件按节检索可靠。  
**失败处理：** 改进正则锚点；重归一化 SEC 文档。  
**严重性：** **BLOCKING**

* * *

### L. 评测种子集完整性（检索就绪）

**脚本：** `qa_scripts/qa_eval_seed_validate.py`  
**读取：** `data/interim/eval/salesforce_eval_seed.jsonl`、分块  
**写入：** `qa_data/outputs/eval_seed_report.json`  
**检查：** 每个 `expected_chunk_id` 存在；所有关键词在该块中出现；分布均衡（SEC ≥ 10，PR ≥ 10，product/docs/help ≥ 8，wiki ≥ 2；每画像 ≥ 10）  
**为什么：** 确保第二天的检索指标有意义。  
**失败处理：** 从相同来源类型自动替换失败样本；重建平衡。  
**严重性：** **BLOCKING**

* * *

### M. 关卡聚合（单一决策）

**脚本：** `qa_scripts/qa_verification_gate.py`  
**读取：** 所有 `qa_data/outputs/*.json`  
**写入：** `qa_data/outputs/verification_gate.json`，包含 PASS/FAIL 与阻断原因  
**为什么：** 一键决定是否推进。  
**严重性：** **BLOCKING**

* * *

### N. 回归包（任何修复之后）

**脚本：** `qa_scripts/qa_regression_pack.py`  
**读取：** 之前 vs 当前 QA 输出  
**写入：** `qa_data/outputs/regression_pack.json`  
**为什么：** 确保修复（如新增模板规则）没有在日期/链接/分节上回退。  
**严重性：** **ADVISORY**，但强烈建议在任何整改后运行

* * *

专门对应你提到的问题
----------

*   **重复率 > 15%** → 运行 **F → G**（先挖模板，再去重网格），应用 allowlist 规则，仅对 **press/product** 重归一化，然后用 **0.90/5** 重去重，再跑 gate。
*   **可能的抽取错误 / 乱码** → **C + D** 捕捉日期/标题/URL 不匹配与编码/乱码；配合 **E** 确保分块边界正确。

* * *

2) 在下一步之前你应该运行的 **快速测试**（重要且省时）
===============================

按顺序跑这套最小集；它以最少运行时捕捉最大阻断风险。如果都绿灯，你就可以安全进入索引与路由开发，同时并行修建议项。

**快速序列与通过门槛**

1.  **基线：**
    *   `python qa_scripts/qa_ground_truth_builder.py`
    *   _原因：_ 后续元数据校验的前置。
2.  **架构与元数据体检：**
    *   `python qa_scripts/qa_schema_validate.py` → **≥ 98% valid**
    *   `python qa_scripts/qa_metadata_validate.py` → **date ≥ 97%**、**title ≥ 98%**、**domains 100%**
    *   _原因：_ 确保结构与时间戳不会毒化排序。
3.  **文本与分块（快速阻断）：**
    *   `python qa_scripts/qa_text_quality.py` → 可打印 ≥ **0.995**，`�`\-free ≥ **99%**
    *   `python qa_scripts/qa_chunk_quality.py` → 长度/重叠达标；**0** 个 SEC 边界跨越
    *   _原因：_ 确保向量不会“垃圾进”。
4.  **重复（你当前的红旗）：**
    *   `python qa_scripts/qa_boilerplate_mine.py`（发现）
    *   `python qa_scripts/qa_dedupe_audit.py` → 使用推荐设置达 **≤ 15%**（优先：过滤模板 + **0.90/5**）
    *   如果仍 > 15%：应用 allowlist，仅对 **press/product** 重归一化，重跑去重审计。
    *   _原因：_ 防止索引过度修剪或暴涨。
5.  **覆盖 + 评测就绪：**
    *   `python qa_scripts/qa_coverage_report.py` → 近 12 个月 PR ≥ **8**；SEC 有 10-K + 10-Q + 8-K
    *   `python qa_scripts/qa_eval_seed_validate.py` → **100% 配对有效**，分布均衡
    *   _原因：_ 确认明天就能跑 Recall/nDCG，而不需返工。
6.  **关卡：**
    *   `python qa_scripts/qa_verification_gate.py` → **PASS**
    *   _原因：_ 输出一份可附带交付的单点决策工件。

**如果在继续前只能修一件事：**  
通过 **模板挖掘 → 归一化 allowlist → 0.90/5 去重** 解决重复，然后重跑 **gate**。这是最可能提升检索质量、降低索引成本的单一改动。

* * *

为什么是这些快速测试
----------

*   **Schema+metadata** 是最常见的“无声失败”，后面常被误以为“排序不好”。
*   **Text & chunks** 确保嵌入不会被垃圾数据污染。
*   **Duplicates** 直接影响成本/延迟与评测公正性。
*   **Coverage+eval seed** 保证你明天无需返工就能跑指标。
*   **Gate** 让推进决策明确而可审计。

* * *

如果你需要，我也可以给每个 JSON 报告的“解读指南”（先看哪些字段、什么范围有问题），但上面两份清单已经足以让你稳妥进入下一阶段。



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)