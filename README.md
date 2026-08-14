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
- An [OpenAI API key](https://platform.openai.com/api-keys) (the agents use GPT-4o-mini and OpenAI embeddings by default)
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

- **Model:** All agents default to `gpt-4o-mini`. Change the `ChatOpenAI(model=...)` argument in
  `agents/climate_agents.py` to use a different model.
- **Local models:** CrewAI supports local models via [Ollama](https://ollama.com/). Pass an Ollama
  LLM instance to the `llm=` argument of an agent to run it locally.

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
- Japan Exchange Group (JPX) (2024, March). *Automated Determination of TCFD Recommended Disclosures
  through Zero-shot Text Classification Using LLMs.* JPX Working Paper Vol. 43.
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
