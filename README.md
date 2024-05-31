# AI ESG Report Builder

Welcome to the AI ESG Report Builder repository! This project showcases the power of AI-ready data management by automating and enhancing Environmental, Social, and Governance (ESG) reporting. The solution leverages a combination of data from gather360, natural language processing with OpenAI's GPT, and Streamlit for an interactive user interface.

## Context and Background

### About the Project

The AI ESG Report Builder tool is designed to simplify and improve the generation of ESG reports. ESG reporting is critical for companies to assess and communicate their impact on environmental, social, and governance factors. Traditionally, creating these reports is time-consuming and resource-intensive. Our solution automates this process, saving time and ensuring accuracy and consistency.

### Inspiration and Development

I’m Tony, the Applied AI Lead at a stealth startup in Dublin. Our mission is to make AI more robust and trustworthy by leveraging a unique data supply chain platform. 


### Our Mission
I work at a mission-driven company.
We believe that data is key to successful AI business implementation.
The current state of business data consistently falls short of what AI needs to deliver its full potential. This gap is where our data supply chain comes into play. We aim to create a consistent, reliable interface for accessing and utilising data, ensuring it is enriched with context, history, provenance, and attribution. This approach transforms data into a powerful asset that AI can leverage with confidence and trustworthiness.

### The Thesis
Our thesis is simple yet profound: The right data unlocks AI's potential. By providing AI with well-structured, contextualised data, we can enable organisations to deploy AI solutions that are not only effective but also transparent and verifiable. This leads to better decision-making, optimised operations, and greater success. We want to democratise AI by making it easier for organisations without deep AI expertise to realise its benefits.

## Key Features

1. **Data Integration**: Connects to gather360 to fetch survey data.
2. **Data Processing**: Processes survey data to generate detailed reports.
3. **AI-Powered Reporting**: Uses OpenAI's GPT to create comprehensive ESG reports.
4. **User-Friendly Interface**: Built with Streamlit for easy interaction and report generation.

## How It Works

### Data Flow

1. **Input Credentials**: Users input their gather360 and OpenAI credentials via the Streamlit sidebar.
2. **Fetch Data**: The app fetches survey data from gather360.
3. **Process Data**: Processes the data according to predefined mappings of questions and answers.
4. **Generate Report**: Uses OpenAI's GPT to generate a detailed ESG report, comparing selected company data with cohort data.
5. **Download Report**: Users can download the generated report in Markdown format.

### Main Components

- **Streamlit Interface**: For user input and report generation.
- **gather360 Connector**: For fetching survey data.
- **Data Processing Functions**: To handle and process survey responses.
- **OpenAI Integration**: For generating narrative reports based on processed data.

## Installation

You can directly use the app without cloning the repository by visiting [the web app page](https://esg-solution.streamlit.app/).

If you still want to run it locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/tonyohalloran/ESG-Solution.git
   cd ESG-Solution
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Data Setup and Getting Credentials 
**Sign Up for Gather360 Trial**
- Visit Gather360: Go to the gather360 signup [link](https://app.g360.io/signup) 
- Sign Up: Sign up for a trial account by providing the required information.
- Activate Account: Check your email for an activation link and complete the registration process.

**Access the ESG Recipe on Gather360**
- Login: Login to your gather360 account.
- Navigate to Recipes: Go to the 'Recipes' section from the dashboard.
- Select ESG Recipe: Find and select the ESG reporting recipe.
  
**Upload Sample Data to Gather360**
- Prepare Data: Ensure your sample data is formatted according to gather360's requirements.
- Upload Data: Use the data upload feature within the ESG recipe to upload your sample data.

**Obtain Gather360 Credentials**
- Go to Settings: In gather360, navigate to the 'Workplace Settings' section and then select 'Connection'.
- API Keys: Locate the API keys section to find your credentials (user, password, account, warehouse, database, schema).

- Obtain OpenAI Credentials
- Visit OpenAI: Go to the OpenAI website.
- Sign In/Sign Up: Sign in to your account or sign up if you don’t have one.
- API Keys: Navigate to the API section to retrieve your API key.


## Usage

1. **Input Credentials**: Enter your gather360 and OpenAI credentials in the sidebar.
2. **Select Company**: Choose the company for which you want to generate the report.
3. **Generate Report**: Click on 'Generate Report for Selected Company' to create a report.
4. **Download Report**: Once generated, download the report as a Markdown file.

## gather360

gather360 is our innovative data supply chain platform that ensures data is enriched with context, supply status and attribution. This approach transforms data into a powerful asset that AI can leverage with confidence and trustworthiness. By providing AI with well-structured, contextualized data, we enable organizations to deploy AI solutions that are not only effective but also transparent and verifiable. This leads to better decision-making, optimized operations, and greater success.

## Contributing

We welcome contributions from the community. If you have suggestions or improvements, please create a pull request or open an issue.

## Join Us

We are building a community of AI and data enthusiasts committed to advancing AI through better data. Join us to share ideas, discuss challenges, and develop solutions together. Together, we can unlock the full potential of AI for businesses worldwide.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Join the Waitlist

Be the first to experience the transformative power of our AI-ready data platform. [Join the waitlist](https://tonyohalloran.ie/).

