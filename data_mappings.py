        actions based on the survey data.*
        *Format your report in markdown to highlight important points and structure the narrative clearly.*
        *Ensure each fact is properly sourced and include attributions in the footnotes. Use the provided raw survey data and calculation details to explain the exact data points used to get a statistic.*
        **Detailed Report Instructions:**
        1. **Cover Page:**
           - Provide a cover page.
           The current date is
           ```
           {today_date}
           ```
           and the report is being prepared for ACT Venture Capital
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
        {pages[0]}
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
