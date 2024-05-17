import streamlit as st
import snowflake.connector
import pandas as pd
from openai import OpenAI
from data_mappings import question_answer_mapping
from io import BytesIO
from datetime import datetime

def get_today_date():
    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    return today_str

st.set_page_config(page_title="ESG Reporting Survey Analysis", layout="wide")

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'creds' not in st.session_state:
    st.session_state.creds = {}
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'thread' not in st.session_state:
    st.session_state.thread = None
if 'assistant' not in st.session_state:
    st.session_state.assistant = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""

with st.sidebar:
    st.header('g360 Credentials')
    user = st.text_input('User', st.session_state.creds.get('user', ''))
    password = st.text_input('Password', type='password', value=st.session_state.creds.get('password', ''))
    account = st.text_input('Account', st.session_state.creds.get('account', ''))
    warehouse = st.text_input('Warehouse', st.session_state.creds.get('warehouse', ''))
    database = st.text_input('Database', st.session_state.creds.get('database', ''))
    schema = st.text_input('Schema', st.session_state.creds.get('schema', ''))

    st.header('OpenAI API Key')
    openai_api_key = st.text_input('API Key', type='password', value=st.session_state.openai_api_key)

    def update_creds():
        st.session_state.creds.update({
            "user": user,
            "password": password,
            "account": account,
            "warehouse": warehouse,
            "database": database,
            "schema": schema
        })
        st.session_state.openai_api_key = openai_api_key

    if st.button('Update Credentials'):
        update_creds()

if not all(st.session_state.creds.values()):
    st.error("Please enter all credentials.")
    st.stop()

if not st.session_state.openai_api_key:
    st.error("Please enter your credentials.")
    st.stop()

client = OpenAI(api_key=st.session_state.openai_api_key)

st.header('ESG Report Generation')
companies = [f'Company {i}' for i in range(1, 38)]
selected_company = st.selectbox('Select Company', companies)

def fetch_data_from_snowflake(query):
    creds = st.session_state.creds
    conn = snowflake.connector.connect(
        user=creds["user"],
        password=creds["password"],
        account=creds["account"],
        warehouse=creds["warehouse"],
        database=creds["database"],
        schema=creds["schema"]
    )
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        return df
    finally:
        cur.close()
        conn.close()

def process_survey_data(survey_data, question_answer_mapping):
    results = {}
    for question, allowed_answers in question_answer_mapping.items():
        filtered_data = survey_data[survey_data['QUESTIONS'] == question]
        answer_counts = filtered_data['RESPONSES'].value_counts()
        total_responses = sum(answer_counts.values)
        results[question] = {"Answers": {}}
        for answer in allowed_answers:
            count = answer_counts.get(answer, 0)
            percentage = (count / total_responses) * 100 if total_responses > 0 else 0
            results[question]["Answers"][answer] = {"count": count, "percentage": percentage}
    return results

def compare_company_to_cohort(company_id, survey_data, question_answer_mapping):
    company_data = survey_data[survey_data['COMPANY_ID'] == company_id]
    cohort_data = survey_data[survey_data['COMPANY_ID'] != company_id]
    
    company_results = process_survey_data(company_data, question_answer_mapping)
    cohort_results = process_survey_data(cohort_data, question_answer_mapping)
    
    comparison_results = {}
    for question in question_answer_mapping.keys():
        comparison_results[question] = {
            "Company": company_results.get(question, {}),
            "Cohort": cohort_results.get(question, {})
        }
    return comparison_results

def generate_company_report(company_id):
    with st.spinner('Generating report for selected company...'):
        with st.spinner('Fetching data from Snowflake...'):
            survey_data = fetch_data_from_snowflake("SELECT * FROM MEASUREMENT_V1_ALL_DATA")

        with st.spinner('Processing survey data...'):
            comparison_results = compare_company_to_cohort(company_id, survey_data, question_answer_mapping)
            today_date = get_today_date()

        # Truncate JSON data to the first 1000 characters
        truncated_data = survey_data.to_json(orient='split')[:1000]

        # Include raw survey data and calculation details
        calculation_details = f"""
        # Calculation Details
        1. **Survey Data Extraction:**
           - The survey data was extracted from the Snowflake database using the query:
           ```
           SELECT * FROM MEASUREMENT_V1_ALL_DATA
           ```
        2. **Processing Survey Data:**
           - For each question, the responses were filtered and counted.
           - Percentages were calculated as (count / total_responses) * 100.
        
        3. **Comparison of Company vs Cohort:**
           - Company data was separated from the cohort data based on the COMPANY_ID.
           - The same processing steps were applied to both company-specific and cohort data.
        Here is the raw survey data in JSON format for your reference:
        ```
        {truncated_data}
        ```
        """

        if st.session_state.assistant is None:
            st.session_state.assistant = client.beta.assistants.create(
                name="ESG Reporting Assistant",
                instructions="You are an assistant generating detailed ESG reports based on survey data. You are extremely fact-based and mention the data/results relevant to a point you make whenever possible. You should always aim to create extremely detailed reports with proper citations.",
                model="gpt-4o"
            )

        if st.session_state.thread is None:
            st.session_state.thread = client.beta.threads.create()

        summary_prompt = f"""
        **Executive Summary of Survey Results for {selected_company}**
        Below is a nested dictionary with the key results of the survey for the selected company compared to the cohort:
        Ensure that there is a clear narrative in the report.
        ```
        {comparison_results}
        ```
        *Please analyze the key trends, raise any critical issues, and suggest actions based on the survey data.*
        *Format your report in markdown to highlight important points and structure the narrative clearly.*
        *Ensure each fact is properly sourced and include attributions in the footnotes. Use the provided raw survey data and calculation details to explain the exact data points used to get a statistic.*
        **Detailed Report Instructions:**
        1. **Cover Page:**
           - Provide a cover page.
           The current date is
           ```
           {today_date}
           ```
           and the report is being prepared for UNAMED Venture Capital
        2. **Key Findings:**
           - Summarize the most important results.
           - Highlight significant trends and patterns.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        3. **Environmental, Social, and Governance (ESG) Analysis:**
           - **Environmental:**
             - Analyze the survey data related to environmental factors.
             - Discuss key findings, trends, and implications.
             - Highlight any critical issues and suggest recommendations.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Social:**
             - Analyze the survey data related to social factors.
             - Discuss key findings, trends, and implications.
             - Highlight any critical issues and suggest recommendations.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Governance:**
             - Analyze the survey data related to governance factors.
             - Discuss key findings, trends, and implications.
             - Highlight any critical issues and suggest recommendations.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
        4. **SWOT Analysis:**
           - **Strengths:**
             - Identify and discuss the strengths revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Weaknesses:**
             - Identify and discuss the weaknesses revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Opportunities:**
             - Identify and discuss the opportunities revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Threats:**
             - Identify and discuss the threats revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
        5. **Critical Issues:**
           - Point out any critical issues raised by the survey.
           - Discuss potential impacts and risks associated with these issues.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        6. **Recommendations:**
           - Provide actionable recommendations based on the survey data.
           - Suggest specific steps or strategies to address the issues identified.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        7. **Conclusion:**
           - Summarize the key takeaways from the report.
           - Reiterate the importance of addressing the identified issues and implementing the recommendations.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        **Calculation Details:**
        {calculation_details}
        """

        st.session_state.conversation_history.append({"role": "user", "content": summary_prompt})

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=summary_prompt
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
            if messages.data:
                for message in messages.data:
                    if message.role == "assistant":
                        summary_content = "".join([block.text.value for block in message.content if block.type == "text"]).strip()  # Extract the text content

                        st.session_state.conversation_history.append({"role": "assistant", "content": summary_content})
                        st.session_state.messages.append({"role": "assistant", "content": summary_content})
                        st.session_state.report_content = summary_content  # Store the report content
                        st.session_state.report_generated = True  # Update the report generated status
                        break
            else:
                st.error("No messages found in the thread.")
        else:
            st.error(f"Report generation failed with status: {run.status}")

def generate_report():
    with st.spinner('Generating report...'):
        with st.spinner('Fetching data from Snowflake...'):
            survey_data = fetch_data_from_snowflake("SELECT * FROM MEASUREMENT_V1_ALL_DATA")

        with st.spinner('Processing survey data...'):
            processed_data = process_survey_data(survey_data, question_answer_mapping)
            today_date = get_today_date()

        # Truncate JSON data to the first 1000 characters
        truncated_data = survey_data.to_json(orient='split')[:1000]

        # Include raw survey data and calculation details
        calculation_details = f"""
        # Calculation Details
        1. **Survey Data Extraction:**
           - The survey data was extracted from the Snowflake database using the query:
           ```
           SELECT * FROM MEASUREMENT_V1_ALL_DATA
           ```
        2. **Processing Survey Data:**
           - For each question, the responses were filtered and counted.
           - Percentages were calculated as (count / total_responses) * 100.
        
        3. **Comparison of Company vs Cohort:**
           - Company data was separated from the cohort data based on the COMPANY_ID.
           - The same processing steps were applied to both company-specific and cohort data.
        Here is the raw survey data in JSON format for your reference:
        ```
        {truncated_data}
        ```
        """

        if st.session_state.assistant is None:
            st.session_state.assistant = client.beta.assistants.create(
                name="ESG Reporting Assistant",
                instructions="You are an assistant generating detailed ESG reports based on survey data. You are extremely fact-based and mention the data/results relevant to a point you make whenever possible. You should always aim to create extremely detailed reports with proper citations.",
                model="gpt-4o"
            )

        if st.session_state.thread is None:
            st.session_state.thread = client.beta.threads.create()

        summary_prompt = f"""
        **Executive Summary of Survey Results**
        Below is a nested dictionary with the key results of a survey:
        Ensure that there is a clear narrative in the report.
        ```
        {processed_data}
        ```
        *Please analyze the key trends, raise any critical issues, and suggest actions based on the survey data.*
        *Format your report in markdown to highlight important points and structure the narrative clearly.*
        *Ensure each fact is properly sourced and include attributions in the footnotes. Use the provided raw survey data and calculation details to explain the exact data points used to get a statistic.*
        **Detailed Report Instructions:**
        1. **Cover Page:**
           - Provide a cover page.
           The current date is
           ```
           {today_date}
           ```
           and the report is being prepared for UNAMED Venture Capital
        2. **Key Findings:**
           - Summarize the most important results.
           - Highlight significant trends and patterns.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        3. **Environmental, Social, and Governance (ESG) Analysis:**
           - **Environmental:**
             - Analyze the survey data related to environmental factors.
             - Discuss key findings, trends, and implications.
             - Highlight any critical issues and suggest recommendations.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Social:**
             - Analyze the survey data related to social factors.
             - Discuss key findings, trends, and implications.
             - Highlight any critical issues and suggest recommendations.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Governance:**
             - Analyze the survey data related to governance factors.
             - Discuss key findings, trends, and implications.
             - Highlight any critical issues and suggest recommendations.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
        4. **SWOT Analysis:**
           - **Strengths:**
             - Identify and discuss the strengths revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Weaknesses:**
             - Identify and discuss the weaknesses revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Opportunities:**
             - Identify and discuss the opportunities revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
           - **Threats:**
             - Identify and discuss the threats revealed by the survey data.
             - Ensure each fact is properly sourced and include attributions in the footnotes.
        5. **Critical Issues:**
           - Point out any critical issues raised by the survey.
           - Discuss potential impacts and risks associated with these issues.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        6. **Recommendations:**
           - Provide actionable recommendations based on the survey data.
           - Suggest specific steps or strategies to address the issues identified.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        7. **Conclusion:**
           - Summarize the key takeaways from the report.
           - Reiterate the importance of addressing the identified issues and implementing the recommendations.
           - Ensure each fact is properly sourced and include attributions in the footnotes.
        **Calculation Details:**
        {calculation_details}
        """

        st.session_state.conversation_history.append({"role": "user", "content": summary_prompt})

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=summary_prompt
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
            if messages.data:
                for message in messages.data:
                    if message.role == "assistant":
                        summary_content = "".join([block.text.value for block in message.content if block.type == "text"]).strip()  # Extract the text content

                        st.session_state.conversation_history.append({"role": "assistant", "content": summary_content})
                        st.session_state.messages.append({"role": "assistant", "content": summary_content})
                        st.session_state.report_content = summary_content  # Store the report content
                        st.session_state.report_generated = True  # Update the report generated status
                        break
            else:
                st.error("No messages found in the thread.")
        else:
            st.error(f"Report generation failed with status: {run.status}")

if st.button('Generate Summary Report for All Companies'):
    generate_report()

if st.button('Generate Report for Selected Company'):
    company_id = int(selected_company.split()[-1])
    generate_company_report(company_id)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    if st.session_state.report_generated and st.session_state.report_content:
        report_bytes = st.session_state.report_content.encode('utf-8')
        report_buffer = BytesIO(report_bytes)

        st.download_button(
            label="Download Report as Markdown",
            data=report_buffer,
            file_name="esg_report.md",
            mime="text/markdown"
        )

if st.session_state.report_generated:
    st.header("Ask Follow-up Questions")
    user_question = st.chat_input("Enter your question related to the report:")
    if user_question:
        st.session_state.conversation_history.append({"role": "user", "content": user_question})
        st.session_state.messages.append({"role": "user", "content": user_question})

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_question
        )

        with st.spinner('Generating response...'):
            run = client.beta.threads.runs.create_and_poll(
                thread_id=st.session_state.thread.id,
                assistant_id=st.session_state.assistant.id,
            )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
            if messages.data:
                for message in messages.data:
                    if message.role == "assistant":
                        follow_up_content = "".join([block.text.value for block in message.content if block.type == "text"]).strip()  # Extract the text content

                        st.session_state.messages.append({"role": "assistant", "content": follow_up_content})
                        st.write(follow_up_content)
                        break
            else:
                st.error("No messages found in the thread.")
        else:
            st.error(f"Follow-up question failed with status: {run.status}")
