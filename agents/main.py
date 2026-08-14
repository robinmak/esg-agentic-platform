import argparse
import os
from textwrap import dedent

from crewai import Crew
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

# Load API keys from a local .env file (see .env.example for the required keys).
# Never hardcode credentials in source.
load_dotenv()


class ClimateCrew:

  def __init__(self, company):
    self.company = company

  def run(self):
    # Imported here (after report paths are set in the environment) so that
    # ClimateAgents picks up the configured TCFD_* paths at import time.
    from climate_agents import ClimateAgents
    from climate_tasks import ClimateTasks

    agents = ClimateAgents()
    tasks = ClimateTasks()

    ######################## Agents ########################
    data_analyst_agent = agents.data_analyst_agent()
    research_analyst_agent = agents.research_analyst_agent()
    filings_agent = agents.filings_analyst_agent()
    assessor_agent = agents.assessor_agent()
    grader_agent = agents.grader_agent()

    ######################## Tasks ########################
    read_tcfd_rec_task = tasks.read_tcfd_rec_task(data_analyst_agent)
    sustainability_data_analysis_task = tasks.sustainability_data_analysis_task(research_analyst_agent)
    filings_data_analysis_task = tasks.filings_data_analysis_task(filings_agent)
    scoring_task = tasks.scoring_task(assessor_agent)
    grading_task = tasks.grading_task(grader_agent)

    ######################## Crew ########################
    crew = Crew(
      agents=[
        data_analyst_agent,
        research_analyst_agent,
        filings_agent,
        assessor_agent,
        grader_agent,
      ],
      tasks=[
        read_tcfd_rec_task,
        sustainability_data_analysis_task,
        filings_data_analysis_task,
        scoring_task,
        grading_task,
        ],
      # manager_llm=ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0.7),
      verbose=True
    )

    result = crew.kickoff()
    return result


def parse_args():
  parser = argparse.ArgumentParser(
    description="Assess a company's TCFD climate disclosures with a crew of AI agents.")
  parser.add_argument(
    "--company",
    help="Name of the company whose TCFD disclosure you want to review.")
  parser.add_argument(
    "--sustainability-report",
    help="Path to the company's ESG/CSR/sustainability/TCFD report PDF. "
         "Overrides the TCFD_SUSTAINABILITY_REPORT environment variable.")
  parser.add_argument(
    "--annual-report",
    help="Path to the company's annual report PDF. "
         "Overrides the TCFD_ANNUAL_REPORT environment variable.")
  return parser.parse_args()


if __name__ == "__main__":
  print("## Welcome to Climate Crew")
  print('-------------------------------')

  args = parse_args()

  # Report paths: CLI arg takes precedence, then any existing env var, then a prompt.
  sustainability_report = args.sustainability_report or os.environ.get("TCFD_SUSTAINABILITY_REPORT")
  if not sustainability_report:
    sustainability_report = input(
      "Path to the company's sustainability/TCFD report PDF: ").strip()

  annual_report = args.annual_report or os.environ.get("TCFD_ANNUAL_REPORT")
  if not annual_report:
    annual_report = input(
      "Path to the company's annual report PDF: ").strip()

  # Publish the paths for climate_agents to read at import time.
  os.environ["TCFD_SUSTAINABILITY_REPORT"] = sustainability_report
  os.environ["TCFD_ANNUAL_REPORT"] = annual_report

  company = args.company
  if not company:
    company = input(
      dedent("""
        Which company TCFD disclosure would you like to review?
      """)).strip()

  climate_crew = ClimateCrew(company)
  result = climate_crew.run()
  print("\n\n########################")
  print("## Here is your TCFD Report")
  print("########################\n")
  print(result)
