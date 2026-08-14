from crewai import Task
from textwrap import dedent
from datetime import date

class ClimateTasks:

    def read_tcfd_rec_task(self, agent):
        return Task(
            description=dedent(f"""
                Read the data from CSV and provide insights on the Task Force on Climate-related Financial Disclosures (TCFD) 
                recommended disclosure criterion definition, and corresponding TCFD recommended disclosure item definition and core 
                element definition.
            """),
            agent=agent,
            expected_output="Comprehensive report presented in a tabular format, listing each TCFD recommended disclosure criterion definition, and corresponding TCFD recommended disclosure item definition and core element definition."
        )

    def sustainability_data_analysis_task(self, agent):
        return Task(
            description=dedent(f"""
                Analyze a company's sustainability-related information in ESG/CSR/environmental/sustainability reports, and Task Force on 
                Climate-related Financial Disclosures (TCFD) reports. Based on the definition of each TCFD recommended disclosure criterion, TCFD recommended disclosure item and core element, 
                extract the information from the reports (either presented in text, table, chart, diagram or other visual format) mapping to the definition of the TCFD 
                recommended disclosure criteria, TCFD recommended disclosure items and core elements.
            """),
            agent=agent,
            expected_output="Comprehensive report on the presence of information for each of the TCFD recommended disclosure criterion definitions, and corresponding TCFD recommended disclosure item definitions and core element definitions."
        )
    
    def filings_data_analysis_task(self, agent):
        return Task(
            description=dedent(f"""
                Analyze a company's sustainability-related information in annual reports. Based on the definition of each TCFD recommended 
                disclosure criterion, TCFD recommended disclosure item and core element, extract the information from the reports (either presented in text, table, chart, diagram or other visual format) mapping to the definition of the TCFD 
                recommended disclosure criteria, TCFD recommended disclosure items and core elements.
            """),
            agent=agent,
            expected_output="Comprehensive report on the presence of information for each of the TCFD recommended disclosure criterion definitions, and corresponding TCFD recommended disclosure item definitions and core element definitions."
        )
        
    def scoring_rubric_design_task(self, agent):
        return Task(
            description=dedent(f"""
            Read the TCFD Disclosures Rubric elements and details from the CSV and design a robust scoring rubric model to evaluate the 
            quality of TCFD disclosures in companies Sustainability and annual reports.
            """),
            agent=agent,
            expected_output="A robust scoring rubric model for assessing and scoring the quality of TCFD disclosures in companies Sustainability and annual report."
        )
    
    def scoring_task(self, agent):
        return Task(
            description=dedent(f"""
            Given the sources of information from the report listing each TCFD recommended disclosure criterion definition and the 
            report on the presence of sustainability-related information mapping to the TCFD recommended disclosure criterion 
            definitio, perform a systematic assessment on the quality of TCFD disclosures in accordance to the definition of each TCFD 
            recommended disclorure criterion using the scoring rubric model for TCFD disclosures. 
            Firstly, score each of the TCFD disclosure criterion based on the scoring rubric model for TCFD Recommendend Disclosure. Use the following elements from the scoring rubric model for the assessment:
            1. Use Scoring Definition for TCFD Recommended Disclosure Criterion to identify the feature, dimension or scope which to be measured.
            2. Use the Sample TCFD Recommended Disclosure Criterion Answer as model answer for the Scoring Definition for TCFD 
            Recommended Disclosure Criterion and to benchmark the quality or performance standard of the answer
            3. Use the Scoring Method for TCFD Recommended Disclosure Criterion to score each TCFD Recommended Disclosure Criterion 
            between 0 and 4 points.
            Next, add up all the scores for the TCFD Recommended Disclosure Criteria that map to the same TCFD Recommended Disclosure Item as 
            the aggregate score for the TCFD Recommended Disclosure Item.
            Please enforce to the following guidelines in the scoring to achieve an accurate, fair and transparent assessment. 
            1. Scoring must be precise and grounded on specific extracts from the sources of information in the reports to verify its authenticity.
            2. If the scoring cannot be determined with certainty, simply acknowledge the lack of knowledge, rather than fabricating an answer.
            3. Be sceptical to the information disclosed in the report as there might be greenwashing (exaggerating the company's disclosure on TCFD recommendations and criteria). Always answer in a critical tone.
            4. Cheap talks are statements that are costless to make and may not necessarily reflect the true intentions or future actions of the company. Be critical for all cheap talks in the reports.
            5. Always acknowledge that the information provided is representing the company's view based on its report.
            6. Scrutinize whether the report is grounded in quantifiable, concrete data or vague, unverifiable statements, and present the findings.
            7. Always complement the assessment and scoring with a short explanation that summarizes the sources in an informative way, i.e. provide details.
            """),
            agent=agent,
            expected_output="A comprehensive report structured with one section detailing the score for each of the 29 TCFD Recommended Disclosure Criterion with explanation, and another section detailing the score for each of the 11 TCFD Recommended Disclosure Item aggregated from the TCFD Recommended Disclosure Criterion."
        )
            
    def grading_task(self, agent):
        return Task(
            description=dedent(f"""
            Read the TCFD Disclosures Grading elements and details from the CSV and design a robust scoring rubric model to grade the TCF disclosures 
            based on the aggregate score of the TCFD Recommended Disclosure Items in the report.
            Then, add up all the aggregate scores for the TCFD Recommended Disclosure Items as overall TCFD Disclosures score. 
            Next, assign the grade for overall TCFD Disclosures score by referring to the grade matching the TCFD Disclosures scores in the scoring rubric model. 
            """),
            agent=agent,
            # expected_output="A comprehensive report on the grade assigned (A, B, C or D) and overall TCFD Disclosures score obtained (between 0 and 116 points). Structure the report by including one section detailing the score for each of the 29 TCFD Recommended Disclosure Criterion with explanation, and another section detailing the score for each of the 11 TCFD Recommended Disclosure Item aggregated from the TCFD Recommended Disclosure Criterion."
            expected_output="A comprehensive report on the grade assigned (A, B, C or D) and overall TCFD Disclosures score obtained (between 0 and 116 points). Structure the report by including one section detailing the score for each of the 29 TCFD Recommended Disclosure Criterion with explanation, and another section detailing the score for each of the 11 TCFD Recommended Disclosure Item aggregated from the TCFD Recommended Disclosure Criterion."
        )