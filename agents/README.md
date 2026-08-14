# agents/

This directory contains the CrewAI agent implementation for the ESG Agentic Platform.

See the [top-level README](../README.md) for a full overview, setup instructions, and usage.

## Files

- `main.py` — CLI entry point (`python main.py`)
- `streamlit_app.py` — Streamlit web UI (`streamlit run streamlit_app.py`)
- `climate_agents.py` — definitions of the five TCFD assessment agents
- `climate_tasks.py` — task/prompt definitions for each agent
- `pdf_tools.py`, `tools/` — tools used by the agents (PDF search, web search, CSV loading, etc.)
- `tcfd_disclosure_criteria.csv` — TCFD recommended disclosure criteria and definitions
- `tcfd_disclosure_rubric.csv` — scoring rubric used by the assessor agent
- `tcfd_disclosure_grading.csv` — grading scale used by the grader agent

> Report PDFs are not included in the repository. Supply your own via the `TCFD_SUSTAINABILITY_REPORT`
> and `TCFD_ANNUAL_REPORT` environment variables, CLI flags, or the Streamlit uploader — no code changes
> needed. See the top-level README for details.
