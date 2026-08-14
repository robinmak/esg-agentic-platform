import os

from crewai import Agent
from crewai_tools import (CSVSearchTool, FileReadTool, PDFSearchTool)
from langchain_openai import ChatOpenAI
import re
import streamlit as st

from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.load_tools import LoadTools
# from tools.browser_tools import BrowserTools
# from tools.pdf_tools import PdfTools

# ---- Configurable input paths --------------------------------------------
# Report PDFs are supplied by the user (they are not shipped with the repo).
# Paths are read from environment variables so the code works out-of-the-box
# for anyone; callers (main.py / streamlit_app.py) may set these from CLI
# arguments or a file uploader before the agents are constructed.
#
#   TCFD_SUSTAINABILITY_REPORT  ESG/CSR/sustainability/TCFD report PDF
#   TCFD_ANNUAL_REPORT          annual report PDF
#
# The TCFD rubric CSVs below ship with the repo; override only if you move them.
# These are resolved lazily (at agent-construction time) so that callers can
# set the environment variables at any point before building the crew,
# regardless of when this module was imported.

def _sustainability_report_path():
  return os.environ.get("TCFD_SUSTAINABILITY_REPORT", "./sustainability_report.pdf")


def _annual_report_path():
  return os.environ.get("TCFD_ANNUAL_REPORT", "./annual_report.pdf")


def _criteria_csv_path():
  return os.environ.get("TCFD_CRITERIA_CSV", "./tcfd_disclosure_criteria.csv")


def _rubric_csv_path():
  return os.environ.get("TCFD_RUBRIC_CSV", "./tcfd_disclosure_rubric.csv")


def _grading_csv_path():
  return os.environ.get("TCFD_GRADING_CSV", "./tcfd_disclosure_grading.csv")


def _pdf_search_tool(pdf_path):
  """Build a PDFSearchTool for `pdf_path` with the shared OpenAI RAG config."""
  return PDFSearchTool(
      pdf=pdf_path,
      config=dict(
          llm=dict(
              provider="openai",
              config=dict(
                  model="gpt-4o-mini-2024-07-18",
                  temperature=0.5,
                  top_p=1,
                  stream=True,
              ),
          ),
          embedder=dict(
              provider="openai",
              config=dict(
                  model="text-embedding-3-small",
              ),
          ),
      ),
  )


class ClimateAgents():

  def __init__(self):
    self.OpenAIGPT4Mini = ChatOpenAI(
        model = "gpt-4o-mini-2024-07-18", temperature=0.7)
  
  def data_analyst_agent(self):
    return Agent(
        role="TCFD Data Analyst",
        goal="""Identify the list of TCFD Recommended Disclosure Criteria and their definitions from the CSV file, including 
        the TCFD Recommended Disclosure Definition and Core Element Definition mapped to each TCFD Recommended Disclosure Criteria.""",
        backstory="""Specializing in Climate-related Financial Disclosures (TCFD), this agent has a knack for organizing 
        and interpreting TCFD framework and data to help public companies and other organizations disclose climate-related risks and opportunities.""",
        tools=[
          FileReadTool(file_path=_criteria_csv_path())
        ],
        # Search CSV content,
        verbose=True,
        llm=self.OpenAIGPT4Mini)
      
  def research_analyst_agent(self):
    return Agent(
        role="TCFD Disclosure Research Analyst",
        goal="""Retrieve and analyze a company's ESG/CSR/environmental/sustainability reports and Task Force on Climate-related 
        Financial Disclosures (TCFD) reports and identify relevant company sustainability and TCFD information disclosures from the reports.""",
        backstory="""Specializing in Climate-related Financial Disclosures (TCFD), this agent analyzes a company's sustainability 
        information disclosures from the reports and extracts the information related to Climate-related Financial 
        Disclosures (TCFD) from the reports.""",
        tools=[
          _pdf_search_tool(_sustainability_report_path())
        ],
        # Search pdf content,
        verbose=True,
        llm=self.OpenAIGPT4Mini)
    
  def filings_analyst_agent(self):
    return Agent(
    role="Filings Research Analyst",
    goal="""Retrieve and analyze a company's annual reports and identify relevant company sustainability and TCFD information
    disclosures from the reports.""",
    backstory="""Specializing in Climate-related Financial Disclosures (TCFD), this agent analyzes a company's sustainability
    information disclosures from the reports and extracts the information related to Climate-related Financial
    Disclosures (TCFD) from the reports.""",
    tools=[
      _pdf_search_tool(_annual_report_path())
    ],
    # Search pdf content,
    verbose=True,
    llm=self.OpenAIGPT4Mini)
  
  def assessor_agent(self):
    return Agent(
      role='TCFD Disclosure Assessor Specialist',
      goal="""Provide a systematic assessment and scoring of a company's fulfilment of each criterion in the Task Force on Climate-related 
      Financial Disclosures (TCFD) recommended disclosures defined in the CSV file using the information and insights from the 
      TCFD Data Analyst agent, TCFD Disclosure Research Analyst agent and Filings Research Analyst agent.""",
      backstory="""Specializing in Climate-related Financial Disclosures (TCFD), this agent assesses a company's fulfilment of the TCFD  
      recommended disclosure criteria based on the information disclosure related to TCFD in the company's annual securities reports, 
      integrated reports, annual reports, and TCFD reports.""",      
      tools=[
        FileReadTool(file_path=_rubric_csv_path()),
        # CalculatorTools(),
        _pdf_search_tool(_sustainability_report_path())
        ],
        # Search CSV content,
    verbose=True,
    llm=self.OpenAIGPT4Mini)
    
  def grader_agent(self):
    return Agent(
      role="TCFD Disclosure Grading Expert",
      goal="""Provide a systematic grading of a company's overall quality of the TCFD disclosures based on the total score of the 11 
      TCFD Recommended Disclosure Items from the TCFD Disclosure Assessor Specialist agent and using the grading scale defined in the CSV file.""",
      backstory="""Specializing in Climate-related Financial Disclosures (TCFD), this agent grades a company's overall quality of the TCFD  
      based on the total score of the 11 TCFD Recommended Disclosure Items.""",      
      tools=[
        FileReadTool(file_path=_grading_csv_path()),
        # CalculatorTools(),
        ],
        # Search CSV content,
      verbose=True,
      llm=self.OpenAIGPT4Mini)
    
###########################################################################################
# Print agent process to Streamlit app container                                          #
# This portion of the code is adapted from @AbubakrChan; thank you!                       #
# https://github.com/AbubakrChan/crewai-UI-business-product-launch/blob/main/main.py#L210 #
###########################################################################################
class StreamToExpander():
  def __init__(self, expander):
    self.expander = expander
    self.buffer = []
    self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
    self.color_index = 0  # Initialize color index

  def write(self, data):
    # Filter out ANSI escape codes using a regular expression
    cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

    # Check if the data contains 'task' information
    task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
    task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
    task_value = None
    if task_match_object:
      task_value = task_match_object.group(1)
    elif task_match_input:
      task_value = task_match_input.group(1).strip()

    if task_value:
      st.toast(":robot_face: " + task_value)

    # Check if the text contains the specified phrase and apply color
    if "Entering new CrewAgentExecutor chain" in cleaned_data:
      # Apply different color and switch color index
      self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

      cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

    if "TCFD Data Analyst" in cleaned_data:
      # Apply different color 
      cleaned_data = cleaned_data.replace("TCFD Data Analyst", f":{self.colors[self.color_index]}[TCFD Data Analyst]")
    if "TCFD Disclosure Research Analyst" in cleaned_data:
      cleaned_data = cleaned_data.replace("TCFD Disclosure Research Analyst", f":{self.colors[self.color_index]}[TCFD Disclosure Research Analyst]")
    if "Filings Research Analyst" in cleaned_data:
      cleaned_data = cleaned_data.replace("Filings Research Analyst", f":{self.colors[self.color_index]}[Filings Research Analyst]")
    if "TCFD Disclosure Assessor Specialist" in cleaned_data:
      cleaned_data = cleaned_data.replace("TCFD Disclosure Assessor Specialist", f":{self.colors[self.color_index]}[TCFD Disclosure Assessor Specialist]")
    if "TCFD Disclosure Grading Expert" in cleaned_data:
      cleaned_data = cleaned_data.replace("TCFD Disclosure Grading Expert", f":{self.colors[self.color_index]}[TCFD Disclosure Grading Expert]")
    if "Finished chain." in cleaned_data:
      cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

    self.buffer.append(cleaned_data)
    if "\n" in data:
      self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
      self.buffer = []