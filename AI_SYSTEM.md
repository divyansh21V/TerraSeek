# AI_SYSTEM.md — AI/ML System Design

> Last updated: 2026-09-25
> Status: Draft — no decisions confirmed

---

## 1. AI Capabilities Overview

`[ASSUMPTION]` Inferred from "AI-powered" in README.

TerraSeek uses AI for:
1. **Natural Language Understanding** — Parse user queries into structured data requests
2. **Query Planning** — Determine which data sources, bands, and processing steps are needed
3. **Data Reasoning** — Interpret processed satellite data and generate insights
4. **Explanation** — Describe methodology and findings in plain language

---

## 2. AI Architecture

```
User Query (text)
     │
     ▼
┌─────────────────┐
│  NLU / Intent   │  Extract: location, time, data type, analysis goal
│    Extraction   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Query Planner  │  Select: providers, collections, bands, processing ops
│   (AI Agent)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Tool Calling  │  Execute: search, retrieve, process (via service layer)
│   / Execution   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Reasoning /   │  Analyze: interpret raster statistics, detect patterns
│   Analysis      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Response      │  Format: text summary + structured data + references
│   Generation    │
└─────────────────┘
```

---

## 3. LLM Integration

### Provider Strategy
`[OPEN QUESTION]` Which LLM provider(s) to support?

| Option | Pros | Cons | Status |
|---|---|---|---|
| OpenAI (GPT-4o) | Best tool calling, widely used | Proprietary, cost | `[OPEN QUESTION]` |
| Anthropic (Claude) | Strong reasoning | Proprietary, cost | `[OPEN QUESTION]` |
| Google (Gemini) | Multimodal, free tier | API stability | `[OPEN QUESTION]` |
| Local models (Ollama) | Free, private, offline | Lower capability | `[OPEN QUESTION]` |
| Multi-provider | Flexibility | Complexity | `[OPEN QUESTION]` |

### Abstraction Layer
`[ASSUMPTION]` The system should abstract LLM calls behind a common interface:

```python
# Conceptual — not implementation code
class LLMProvider(Protocol):
    async def complete(self, messages: list[Message], tools: list[Tool]) -> Response: ...
    async def embed(self, texts: list[str]) -> list[list[float]]: ...
```

---

## 4. Agent Framework

`[OPEN QUESTION]` Framework selection.

| Option | Notes | Status |
|---|---|---|
| LangChain / LangGraph | Mature, large ecosystem | `[OPEN QUESTION]` |
| LlamaIndex | Strong for RAG | `[OPEN QUESTION]` |
| Custom agent loop | Full control, less dependency | `[OPEN QUESTION]` |
| CrewAI | Multi-agent orchestration | `[OPEN QUESTION]` |
| No framework (direct API) | Simple, but more code | `[OPEN QUESTION]` |

---

## 5. Tools / Function Calling

The AI agent needs access to these tools:

| Tool | Description | Status |
|---|---|---|
| `search_catalogs` | Query STAC catalogs with structured params | `[ASSUMPTION]` |
| `get_dataset_info` | Retrieve metadata for a specific dataset | `[ASSUMPTION]` |
| `download_asset` | Download a specific data file | `[ASSUMPTION]` |
| `compute_index` | Calculate spectral index (NDVI, etc.) | `[ASSUMPTION]` |
| `clip_raster` | Clip raster to geometry | `[ASSUMPTION]` |
| `get_statistics` | Get raster band statistics | `[ASSUMPTION]` |
| `create_composite` | Mosaic multiple scenes | `[ASSUMPTION]` |
| `compare_temporal` | Compare data across time periods | `[ASSUMPTION]` |

---

## 6. Embeddings & Retrieval

`[OPEN QUESTION]` Is RAG needed for TerraSeek?

Possible uses:
- Embedding dataset metadata for semantic search
- Embedding documentation for user help
- Embedding past queries for suggestion/autocomplete

Vector store options: See `ARCHITECTURE.md` technology stack.

---

## 7. Prompt Engineering

`[ASSUMPTION]` Prompts should be:
- Stored as versioned templates, not hardcoded
- Testable with evaluation datasets
- Separated by concern (intent extraction vs. reasoning vs. explanation)

Prompt storage location: `[OPEN QUESTION]` — `terraseek/ai/prompts/` ?

---

## 8. Cost Management

`[OPEN QUESTION]` If using commercial LLMs:

| Concern | Approach | Status |
|---|---|---|
| Token budgets | Per-query token limits | `[OPEN QUESTION]` |
| Caching | Cache LLM responses for identical queries | `[ASSUMPTION]` |
| Model routing | Use cheaper models for simple tasks | `[OPEN QUESTION]` |
| Fallback | Degrade gracefully if LLM unavailable | `[ASSUMPTION]` |

---

## 9. Evaluation

`[OPEN QUESTION]` How to evaluate AI quality?

| Metric | Description | Status |
|---|---|---|
| Intent extraction accuracy | Does parsed query match expected? | `[OPEN QUESTION]` |
| Plan correctness | Are the right tools selected? | `[OPEN QUESTION]` |
| Analysis quality | Are insights accurate and useful? | `[OPEN QUESTION]` |
| Hallucination rate | Does the AI fabricate data? | `[OPEN QUESTION]` |

---

## 10. Risks

| Risk | Impact | Mitigation | Status |
|---|---|---|---|
| LLM hallucination | Wrong data or analysis served to user | Ground all claims in actual data | `[RISK]` |
| API cost overrun | Unexpected bills | Token budgets + monitoring | `[RISK]` |
| Provider lock-in | Can't switch LLMs | Abstraction layer | `[RISK]` |
| Latency | Slow response for complex queries | Streaming + async processing | `[RISK]` |
| Data privacy | User queries sent to external LLM | Local model option | `[RISK]` |

---

## Related Documents

- Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- Security → [SECURITY.md](SECURITY.md)
- Testing → [TESTING.md](TESTING.md)
- Decisions → [DECISIONS.md](DECISIONS.md)
