# Question-answer mapping for processing survey data
question_answer_mapping = {
    'Do you measure your carbon footprint?': ['Yes - Scope 1', 'Yes - Scopes 1 & 2', 'Yes - Scopes 1-3', 'No - but plan to in the next 12 months', 'No'],
    'Do you have a policy and programme in place to achieve net zero carbon? Including a stated date for achieving net zero with specific milestones and monitoring plans.': ['Yes - 2030', 'Yes - Other date (Please indicate date in Column G)', 'No - but plan to in the next 12 months', 'No'],
    'Do you have external carbon certifications for your business, or do you include carbon reporting in your annual external audit?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you use any carbon offsetting tools or initiatives to offset your carbon emissions?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    "What percentage of your office's energy consumption comes from renewable sources? If you do not have an office space, please select not relevant.": ['Not relevant', 'We currently do not track this metric', 'We plan to report this metric in the next 12 months'],
    'What percentage of your employees take part in sustainable travel initiatives?': ['Not relevant', 'We currently do not track this metric', 'We plan to report this metric in the next 12 months', '0%', '1-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
    'Do you have a corporate scheme in place to reduce the emissions of your plane travel?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'Do you have measures to reduce the emissions of your own distribution fleet or do you prioritise logistics companies that have a net zero policy?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'Do you have a policy to reduce or reuse hard to recycle waste?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'What percentage of the packaging you use for your products is recycled or reusable (e.g. via Loop or other schemes)?': ['Not relevant', 'We currently do not track this metric', 'We plan to report this metric in the next 12 months'],
    'What percentage of your procurement spend includes suppliers that are local to your business?': ['Not relevant', 'We currently do not track this metric', 'We plan to report this metric in the next 12 months'],
    'What percentage of your procurement spend goes to suppliers that have you screened for carbon efficiency (e.g., data centres, IT / hosting providers, manufacturers, etc.)?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'If you have your own warehouse / manufacturing facilities, do you have initiatives in place to limit energy and carbon footprint?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'What percentage of your suppliers have you conducted modern slavery due diligence on?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'How many weeks of paid primary carer parental leave do you offer above statutory requirement?': ['We plan to report this metric in the next 12 months', 'Zero', '1501 or more'],
    'How many weeks of paid secondary carer parental leave do you offer above statutory requirement?': ['We plan to report this metric in the next 12 months', 'Zero', '1501 or more'],
    'Do you have return to work initiatives or support in place?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'What percentage of your board identify as female?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your board identify as coming from underrepresented ethnic or cultural backgrounds (as defined in relevant countries of operation)?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your board identify as LGBTQIA+?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your senior management/leadership team identify as female?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your senior management/leadership team identify as coming from underrepresented ethnic or cultural backgrounds (as defined in relevant countries of operation)?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your senior management/leadership team identify as LGBTQIA+?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your total workforce identify as female?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your total workforce identify as coming from underrepresented ethnic or cultural backgrounds (as defined in relevant countries of operation)?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'What percentage of your total workforce identify as LGBTQIA+?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'Do you provide equality, diversity and inclusion training for all of your staff?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Does your office provide an inclusive environment (e.g., disabled access, breastfeeding space, unisex bathrooms)?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'Do you have a recruitment program in place to reach people from diverse backgrounds (e.g., working with specialist head-hunters, partnering with relevant university groups, etc.)?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you offer internships, apprenticeships or trainee programmes?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have a policy or a strategy in place to provide support to staff around mental health and wellbeing?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you offer study support to staff (e.g., financial support, study leave, flexible working opportunities, etc.)?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Are all staff members paid the minimum wage?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'What percentage of your employees are eligible for health care benefits offered by your company?': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'How much have you donated to community projects in the last year? ($/£/€ terms)': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric', '£0', '£1-499', '£500-999', '£1', '000-1', '499', '£1', '500-1', '999', '£2', '000+'],
    'Do you provide paid time off for employees to complete volunteering or community engagement activities?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'What percentage of your board members are independent?': ['Not relevant', 'We currently do not track this metric', 'We plan to report this metric in the next 12 months'],
    'How many board meetings have you held in the previous 12 months?': ['We plan to report this metric in the next 12 months', 'Zero', '1501 or more'],
    'Is sustainability a regular item on your board agenda?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'What is your gender pay gap? (%) Please only complete this metric if you have carried out a full gender pay gap assessment - guidance for this can be found in column H.': ['We plan to report this metric in the next 12 months', 'We currently do not track this metric'],
    'Do you have any initiatives in place to reduce/impact your gender pay gap?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have processes and procedures to ensure compliance with data regulation (e.g., GDPR) and prevent/ monitor unintended uses of data?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'Do you offer staff codes of conduct and relevant training to support the responsible development and use of code/ AI systems?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'What percentage of your staff is trained annually on cybersecurity?': ['We currently do not track this metric', 'We plan to report this metric in the next 12 months', '0%', '1-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
    'Have you set up cyber security controls to monitor risks in the data infrastructure and promptly report/address incidents?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'Do you have an ESG Policy in place?': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant'],
    'Do you conduct an annual diversity and inclusion survey?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have a remote working policy in place?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have a corporate code of ethics/good business conduct policy in place?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have an anti-bribery and/or anti-corruption policy in place?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have a whistle blowing policy in place?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Do you have an anti harassment policy in place?': ['Yes', 'No - but plan to in the next 12 months', 'No'],
    'Have you completed an industry-specific sustainability certification or accreditation? (Please provide details)': ['Yes', 'No - but plan to in the next 12 months', 'No', 'Not relevant']
}
