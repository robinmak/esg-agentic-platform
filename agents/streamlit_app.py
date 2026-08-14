from crewai import Crew
from textwrap import dedent
from climate_agents import ClimateAgents, StreamToExpander
from climate_tasks import ClimateTasks
from langchain_openai import ChatOpenAI
import streamlit as st
import datetime
import os
import sys
import tempfile

from dotenv import load_dotenv

# Load API keys from a local .env file (see .env.example for the required keys).
# Never hardcode credentials in source.
load_dotenv()

st.set_page_config(page_icon="🌍", layout="wide")


def _save_upload(uploaded_file):
    """Persist a Streamlit UploadedFile to a temp path and return that path."""
    suffix = os.path.splitext(uploaded_file.name)[1] or ".pdf"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getbuffer())
    tmp.flush()
    tmp.close()
    return tmp.name


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class ClimateCrew:

    def __init__(self, company):
        self.company = company
        self.output_placeholder = st.empty()

    def run(self):
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
        self.output_placeholder.markdown(result)

        return result


if __name__ == "__main__":
    icon("🌍 ClimateAIgent")

    st.subheader("Welcome to Climate Crew!",
                 divider="rainbow", anchor=False)

    with st.sidebar:
        st.header("👇 Enter your company details")
        with st.form("my_form"):
            company = st.text_input(
                "Which company TCFD disclosure would you like to review?", placeholder="DBS")
            sustainability_report = st.file_uploader(
                "Sustainability / TCFD report (PDF)", type=["pdf"])
            annual_report = st.file_uploader(
                "Annual report (PDF)", type=["pdf"])
            submitted = st.form_submit_button("Submit")

        st.divider()

        # # Credits to joaomdmoura/CrewAI for the code: https://github.com/joaomdmoura/crewAI
        # st.sidebar.markdown(
        # """
        # Credits to [**@joaomdmoura**](https://twitter.com/joaomdmoura)
        # for creating **crewAI** 🚀
        # """,
        #     unsafe_allow_html=True
        # )

        # st.sidebar.info("Click the logo to visit GitHub repo", icon="👇")
        # st.sidebar.markdown(
        #     """
        # <a href="https://github.com/joaomdmoura/crewAI" target="_blank">
        #     <img src="https://raw.githubusercontent.com/joaomdmoura/crewAI/main/docs/crewai_logo.png" alt="CrewAI Logo" style="width:100px;"/>
        # </a>
        # """,
        #     unsafe_allow_html=True
        # )

    if submitted:
        if not sustainability_report or not annual_report:
            st.warning("Please upload both the sustainability/TCFD report and the annual report PDFs.")
        else:
            # Persist uploads and publish their paths for climate_agents to read.
            os.environ["TCFD_SUSTAINABILITY_REPORT"] = _save_upload(sustainability_report)
            os.environ["TCFD_ANNUAL_REPORT"] = _save_upload(annual_report)

            with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
                with st.container(height=500, border=False):
                    sys.stdout = StreamToExpander(st)
                    climate_crew = ClimateCrew(company)
                    result = climate_crew.run()
                status.update(label="✅ TCFD Disclosure Assessment is Ready!",
                            state="complete", expanded=False)

            st.subheader("Here is your TCFD Disclosure Assessment", anchor=False, divider="rainbow")
            st.markdown(result)