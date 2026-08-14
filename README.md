# ESG Agentic Platform

An **agentic AI platform for automated assessment of corporate climate disclosures** against the
[TCFD](https://www.fsb-tcfd.org/) (Task Force on Climate-related Financial Disclosures) recommendations.

The platform orchestrates a crew of role-playing AI agents (built with [CrewAI](https://github.com/crewAIInc/crewAI))
that read a company's sustainability and annual reports, map the contents against the TCFD recommended
disclosure criteria, score each criterion, and produce an overall disclosure grade — helping analysts
evaluate the completeness and quality of climate-related financial disclosures at scale.

> **Disclaimer:** This is a research/experimental project. Its output is an AI-generated assessment and
> should not be treated as professional, financial, legal, or compliance advice. Always have a qualified
> human review the results.

## How it works

Five specialized agents collaborate in a pipeline:

| Agent | Role | Input |
| --- | --- | --- |
| **TCFD Data Analyst** | Loads and interprets the TCFD recommended disclosure criteria and their definitions | `tcfd_disclosure_criteria.csv` |
| **TCFD Disclosure Research Analyst** | Extracts climate-related disclosures from a company's ESG / CSR / sustainability / TCFD reports | Sustainability report PDF |
| **Filings Research Analyst** | Extracts climate-related disclosures from a company's annual report | Annual report PDF |
| **TCFD Disclosure Assessor Specialist** | Scores each of the TCFD recommended disclosure criteria (0–4) against a scoring rubric, critically screening for greenwashing and unsubstantiated "cheap talk" | `tcfd_disclosure_rubric.csv` + report PDFs |
| **TCFD Disclosure Grading Expert** | Aggregates criterion scores into the 11 recommended-disclosure-item scores and assigns an overall grade (A–D) | `tcfd_disclosure_grading.csv` |

The final output is a report containing per-criterion scores with justifications, aggregated
disclosure-item scores, an overall score (0–116), and a letter grade.

### The TCFD reference data

The assessment is driven by three CSV files that ship with the repo. They encode the TCFD framework as a
three-level hierarchy — **Core Element → Recommended Disclosure Item → Recommended Disclosure Criterion** —
plus the rules for scoring and grading:

| File | What it defines | Consumed by |
| --- | --- | --- |
| `tcfd_disclosure_criteria.csv` | The TCFD framework itself: each Core Element, its 11 Recommended Disclosure Items, and the 29 fine-grained Criteria, each with definitions and guidelines. This is the **checklist** of what a company should disclose. | TCFD Data Analyst |
| `tcfd_disclosure_rubric.csv` | For every criterion: a **scoring definition** (what to measure), a **scoring method** (how to assign 0–4), and a **sample answer** (the benchmark for full marks). This turns the checklist into a **gradebook**. | TCFD Disclosure Assessor Specialist |
| `tcfd_disclosure_grading.csv` | The **grade bands** that map a total score (0–116) to a letter grade A–D. | TCFD Disclosure Grading Expert |

So the criteria file says *what* to look for, the report PDFs supply *the evidence*, the rubric says *how
to score each piece of evidence*, and the grading file says *how to turn the total into a grade*.

### How the agents work together

The five agents run as a **sequential pipeline** (defined in `main.py` / `streamlit_app.py`). Each agent's
output becomes context for the ones after it, so knowledge flows left-to-right: the framework is loaded,
evidence is gathered from two report sources, the evidence is scored against the rubric, and the scores are
finally graded.

```mermaid
flowchart TD
    subgraph inputs [Reference data & documents]
        C[tcfd_disclosure_criteria.csv<br/>Core Element - Item - 29 Criteria]
        R[tcfd_disclosure_rubric.csv<br/>scoring definition / method / sample]
        G[tcfd_disclosure_grading.csv<br/>A-D grade bands]
        SR[(Sustainability / TCFD report PDF)]
        AR[(Annual report PDF)]
    end

    C --> A1[1 . TCFD Data Analyst<br/>loads &amp; explains the 29 criteria]
    A1 -- criteria definitions --> A2[2 . Research Analyst<br/>extracts disclosures from sustainability report]
    A1 -- criteria definitions --> A3[3 . Filings Analyst<br/>extracts disclosures from annual report]
    SR --> A2
    AR --> A3

    A2 -- evidence per criterion --> A4[4 . Assessor Specialist<br/>scores each criterion 0-4 vs rubric]
    A3 -- evidence per criterion --> A4
    R --> A4

    A4 -- 29 criterion scores<br/>+ 11 item aggregates --> A5[5 . Grading Expert<br/>totals score, assigns A-D]
    G --> A5
    A5 --> OUT[[TCFD assessment report<br/>scores + justifications + grade]]
```

**Step by step:**

1. **TCFD Data Analyst** reads `tcfd_disclosure_criteria.csv` and produces a structured explanation of the
   29 criteria and their definitions — establishing the shared checklist the downstream agents work against.
2. **Research Analyst** searches the **sustainability / TCFD report** for disclosures that map to each
   criterion, quoting the supporting text.
3. **Filings Analyst** does the same against the **annual report**, so evidence is drawn from both document
   types.
4. **Assessor Specialist** takes the gathered evidence and, using `tcfd_disclosure_rubric.csv`, scores each
   of the 29 criteria **0–4**. For every criterion the rubric supplies three things — a *scoring definition*
   (what to measure), a *scoring method* (how to map the evidence to a 0–4 score), and a *sample answer*
   (the benchmark for full marks) — and the agent critically screens for greenwashing and unsubstantiated
   "cheap talk". It then aggregates the criterion scores into the 11 disclosure-item scores.
   *Input:* evidence from steps 2–3 + the rubric. *Output:* 29 criterion scores + 11 item aggregates.
5. **Grading Expert** sums the 11 item scores into an overall total and maps it to a letter grade using the
   bands in `tcfd_disclosure_grading.csv`. Because there are 29 criteria scored 0–4, the maximum total is
   `29 × 4 = 116`. *Input:* the item scores + the grading bands. *Output:* the overall score and grade.

   | Grade | Overall score |
   | --- | --- |
   | **A** | 87–116 |
   | **B** | 58–86 |
   | **C** | 29–57 |
   | **D** | 0–28 |

### Scoring & grading rubric model

The assessment escalates through three levels — a fine-grained **criterion score** rolls up into a
**disclosure-item aggregate**, and the sum of all items maps to an overall **grade**:

```mermaid
flowchart LR
    A["<b>Score (0–4 points)</b><br/>per TCFD Recommended<br/>Disclosure Criterion<br/><i>29 criteria</i>"]
    B["<b>Aggregate Score</b><br/>per TCFD Recommended<br/>Disclosure Item<br/><i>11 items</i>"]
    C["<b>Grade Scale</b><br/>overall total 0–116<br/><i>A · B · C · D</i>"]
    M["<b>Grading Moderator</b><br/>peer-normalize vs comparable<br/>banks — by size &amp; HQ region<br/><i>(planned extension)</i>"]

    A -- "sum criteria within each item" --> B
    B -- "sum all 11 items → map to band" --> C
    C -. "optional peer benchmarking" .-> M

    classDef done fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
    classDef grade fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef plan fill:#fff8e1,stroke:#c8a020,color:#7a5c00,stroke-dasharray:5 3;
    class A,B done;
    class C grade;
    class M plan;
```

- **Score (0–4)** — the Assessor grades each of the **29 criteria** against `tcfd_disclosure_rubric.csv`.
- **Aggregate Score** — criterion scores are summed within each of the **11 disclosure items**.
- **Grade Scale** — the Grading Expert totals the items (max 116) and assigns **A–D** per
  `tcfd_disclosure_grading.csv`.
- **Grading Moderator** *(planned, not yet in code)* — a further step that normalizes a company's grade
  against comparable peers (e.g. by bank size and HQ region) using the moderating dataset in `references/`.
  This mirrors the design in the [Auzepy et al. (2023)](https://arxiv.org/abs/2302.00326) reference but is
  **not implemented** in the current 5-agent pipeline.

## Project structure

```
esg-agentic-platform/
├── agents/
│   ├── main.py               # CLI entry point
│   ├── streamlit_app.py      # Streamlit web UI
│   ├── climate_agents.py     # Agent definitions (the "crew")
│   ├── climate_tasks.py      # Task/prompt definitions for each agent
│   ├── pdf_tools.py          # PDF search tool
│   ├── tools/                # Search, load, calculator, browser, PDF tools
│   ├── tcfd_disclosure_criteria.csv   # TCFD criteria & definitions
│   ├── tcfd_disclosure_rubric.csv     # Scoring rubric
│   ├── tcfd_disclosure_grading.csv    # Grading scale
│   ├── requirements.txt
│   └── pyproject.toml
├── .env.example              # Template for required API keys
├── .gitignore
├── LICENSE
└── README.md
```

## Prerequisites

- Python **3.10 or 3.11** (see `agents/pyproject.toml`)
- An [OpenAI API key](https://platform.openai.com/api-keys) — used by default (the agents run on GPT-4o-mini
  with OpenAI embeddings). CrewAI is model-agnostic, so this is **not strictly required**: you can swap in
  another LLM instead (e.g. Anthropic Claude, Google Gemini, Azure OpenAI, or a local model via
  [Ollama](https://ollama.com/)). See [Configuration](#configuration) for how to change the model — note
  that the PDF-search tool also uses an embedding model, so a provider offering embeddings (or a separate
  embeddings key) is needed for that step.
- A [Serper API key](https://serper.dev/) (for the internet-search tool)

## Setup

```bash
# 1. Clone
git clone https://github.com/robinmak/esg-agentic-platform.git
cd esg-agentic-platform

# 2. Configure API keys
cp .env.example .env
# then edit .env and fill in your keys

# 3. Install dependencies
cd agents
pip install -r requirements.txt          # or: poetry install --no-root
```

### Provide the report documents

The report PDFs are **not included** in this repository (they are third-party corporate documents and
are excluded via `.gitignore`). Download the two reports you want to analyze and tell the app where they
are — no code changes required. The paths are read from environment variables:

| Variable | What it points to | Default |
| --- | --- | --- |
| `TCFD_SUSTAINABILITY_REPORT` | ESG / CSR / sustainability / TCFD report PDF | `./sustainability_report.pdf` |
| `TCFD_ANNUAL_REPORT` | Annual report PDF | `./annual_report.pdf` |
| `TCFD_CRITERIA_CSV` | TCFD criteria & definitions (ships with repo) | `./tcfd_disclosure_criteria.csv` |
| `TCFD_RUBRIC_CSV` | Scoring rubric (ships with repo) | `./tcfd_disclosure_rubric.csv` |
| `TCFD_GRADING_CSV` | Grading scale (ships with repo) | `./tcfd_disclosure_grading.csv` |

You can set the two report paths in your `.env` file, pass them as CLI arguments, or (in the Streamlit
app) upload the PDFs directly through the browser — see **Running** below. The CSV rubric files ship with
the repo and rarely need to change.

## Running

**CLI** — pass the report paths as flags, or you'll be prompted for them:

```bash
cd agents
python main.py \
  --company "DBS" \
  --sustainability-report /path/to/sustainability_report.pdf \
  --annual-report /path/to/annual_report.pdf

# or just run it and answer the prompts:
python main.py
```

**Streamlit web UI** — enter the company name and upload the two report PDFs in the sidebar:

```bash
cd agents
streamlit run streamlit_app.py
```

> ⚠️ **Cost note:** Running the crew makes multiple calls to the OpenAI API (LLM + embeddings) and will
> incur usage charges on your account.

## Configuration

- **Model:** All agents default to `gpt-4o-mini` via `ChatOpenAI` in `agents/climate_agents.py`. CrewAI is
  model-agnostic, so you can point the agents at a different LLM by replacing the `ChatOpenAI(...)` instance
  passed to each agent's `llm=` argument. For example:
  - **Anthropic Claude** — `from langchain_anthropic import ChatAnthropic; llm = ChatAnthropic(model="<claude-model>")`
  - **Google Gemini** — `from langchain_google_genai import ChatGoogleGenerativeAI; llm = ChatGoogleGenerativeAI(model="<gemini-model>")`
  - **Azure OpenAI** — `from langchain_openai import AzureChatOpenAI`

  Install the matching LangChain integration package and set that provider's API key in your `.env`.
  Pick a current model name from your chosen provider's documentation.
- **Local models:** CrewAI supports local models via [Ollama](https://ollama.com/). Pass an Ollama
  LLM instance to the `llm=` argument of an agent to run it fully offline.
- **Embeddings:** The PDF-search tool (`_pdf_search_tool` in `agents/climate_agents.py`) also uses an
  embedding model — OpenAI's `text-embedding-3-small` by default. If you move off OpenAI entirely, update
  the `embedder` config there to a provider your setup supports (e.g. Ollama or Google embeddings).

## Security

Do **not** commit API keys. Keys are read from a local `.env` file (ignored by git). If you ever expose a
key, rotate it immediately in the provider's dashboard.

## References

This project's approach to automated TCFD disclosure analysis and scoring draws on the following
frameworks, academic research, and datasets. The source documents are kept locally in the `references/`
directory (not committed to the repository, as they are third-party copyrighted material).

**Framework & guidance**

- Task Force on Climate-related Financial Disclosures (TCFD). *Implementing the Recommendations of the
  Task Force on Climate-related Financial Disclosures* (Annex, amended December 2017). Financial Stability
  Board. — `FINAL-TCFD-Annex-Amended-121517.pdf`
- *Financial institutions' climate-related disclosure* guidance document. — `financial-institutions-climate-related-disclosure-document.pdf`

**Academic research**

- Ni, J., Bingler, J., Colesanti-Senni, C., Kraus, M., Gostlow, G., Schimanski, T., Stammbach, D.,
  Ashraf Vaghefi, S., Wang, Q., Webersinke, N., Wekhof, T., Yu, T., & Leippold, M. (2023).
  *CHATREPORT: Democratizing Sustainability Disclosure Analysis through LLM-based Tools.*
  [arXiv:2307.15770](https://arxiv.org/abs/2307.15770). — `CHATREPORT - Democratizing Sustainability Disclosure Analysis.pdf`
- Auzepy, A., Tönjes, E., Lenz, D., & Funk, C. (2023). *Evaluating TCFD Reporting: A New Application of
  Zero-Shot Analysis to Climate-related Financial Disclosures.*
  [arXiv:2302.00326](https://arxiv.org/abs/2302.00326). — `Evaluating TCFD reporting - A new application of zero-shot analysis to climate-related financial disclosures.pdf`
- Doi, N., Oda, Y., Nakakubo, N., & Sugimoto, J. (2024, March 4). *Automated Determination of TCFD
  Recommended Disclosures through Zero-shot Text Classification Using Large Language Models.*
  Japan Exchange Group (JPX) Working Paper Vol. 43.
  [PDF](https://www.jpx.co.jp/english/corporate/research-study/working-paper/JPXWP_Vol43e.pdf) ·
  [news release](https://www.jpx.co.jp/english/corporate/news/news-releases/0010/20240304-01.html).
  — `JPX - Automated Determination of TCFD Recommended Disclosures through Zero-shot Text Classification Using LLMs.pdf`

**Datasets**

- *TCFD disclosures dataset* used for moderating/benchmarking TCFD disclosure scores. —
  `tcfd_disclosures_dataset for moderating TCFD disclosure score.csv`

## Acknowledgements

- Built on the [CrewAI](https://github.com/crewAIInc/crewAI) multi-agent framework.
- The Streamlit output-streaming helper (`StreamToExpander`) is adapted from
  [@AbubakrChan](https://github.com/AbubakrChan/crewai-UI-business-product-launch).
- The TCFD recommendations are published by the [Task Force on Climate-related Financial Disclosures](https://www.fsb-tcfd.org/).

## License

Released under the [MIT License](LICENSE).
