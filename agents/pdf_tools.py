import os

from crewai_tools import PDFSearchTool
from langchain.tools import tool

class PdfTools():
    @tool("Search pdf content")
    def search_pdf():
        """Searches for specific content within a PDF."""
        result = PDFSearchTool(
        pdf=os.environ.get("TCFD_SUSTAINABILITY_REPORT", "./sustainability_report.pdf"),
        config=dict(
            llm=dict(
                provider="openai", # or google, ollama, anthropic, llama2, ...
                config=dict(
                    model="gpt-4o-mini-2024-07-18",
                    temperature=0.5,
                    top_p=1,
                    stream=True,
                ),
            ),
            embedder=dict(
                provider="openai", # or google, ollama, ...
                config=dict(
                    model="text-embedding-3-small",
                    # task_type="retrieval_document",
                    # title="Embeddings",
                ),
            ),
        )
    )
        return (result)
