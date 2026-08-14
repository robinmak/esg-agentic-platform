import os

from langchain.agents import Tool
from langchain.tools import tool
from langchain_community.document_loaders.csv_loader import CSVLoader

class LoadTools():
    @tool("Load csv data")
    def load_csv():
        """Load the CSV data from the source"""
        loader = CSVLoader(
            file_path=os.environ.get("TCFD_CRITERIA_CSV", "./tcfd_disclosure_criteria.csv"))
        csv_data = Tool(
        name="Data Loader Tool",
        func=loader.load,
        description="Load the CSV data from the source",
        )