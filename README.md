# Overview
This project is a Streamlit-based web application developed as part of the thesis *'Political Microtargeting in the Age of Generative AI: Evaluating the Effectiveness of Large Language Models for Targeted Political Messaging'*, which investigates the effectiveness of political microtargeting using Large Language Models (LLMs) such as OpenAI's GPT-4o. The study examines whether targeted political messages, generated in real-time based on the political profiles of participants, are more persuasive than untargeted messages. The application collects demographic and political information, presents dynamically generated political messages to participants, and records their evaluations.

## How It Works

1. Participants start by providing demographic data and answering questions to determine their political profile across multiple dimensions.
2. The app assigns participants to one of three treatment groups: targeted, non-targeted, or false-targeted messaging.
3. Based on their treatment group, political messages are generated in real-time using GPT-4o and displayed to participants.
4. Participants evaluate the persuasiveness of the messages and provide feedback on whether they perceive the message as targeted to them.
5. Data from the survey is stored for analysis, where the effectiveness of microtargeting is compared across different groups and political topics.

## Project Structure

The repository is organized into several key directories and files:

### **analysis/**
Contains scripts and notebooks for analyzing survey data.

- **data_analysis.ipynb**: A Jupyter notebook used for analyzing survey responses and extracting insights about message persuasiveness.
- **functions.py**: Utility functions for data processing and statistical analysis.
- **requirements.txt**: Lists the Python dependencies required for running the data analysis.

### **data/**
Stores the collected survey data.

- **survey_data.csv**: Contains participant responses and evaluation metrics for the study. This file includes data on demographics, political profiles, message evaluations, and perceived targeting.

### **figures/**
Contains figures generated from the data analysis.

### **survey_app/**
This directory contains the main code for the Streamlit web application.

- **.streamlit/**
  - **config.toml**: Configuration file for Streamlit settings, such as UI customizations.
  - **secrets.toml**: File used to securely store API keys, including access to OpenAI’s API.

- **closing_page.py**: Handles the final page of the study, where participants complete the survey.
- **config.py**: Configures the Streamlit application, including setup for page layouts and theme.
- **constants.py**: Stores constants, such as fixed text and option lists, used throughout the app.
- **demographics.py**: Manages the page where participants input demographic data.
- **dimensions.py**: Handles the collection of participants' political beliefs across four dimensions: economic, social, global vs. national sovereignty, and climate policies.
- **feedback.py**: Collects participant feedback on the study process.
- **functions.py**: Contains helper functions, including API call logic and functions to write responses to Google Sheets.
- **introduction.txt**: The introductory text displayed on the start page of the survey.
- **page_template.py**: Template to facilitate the creation of new pages for the application.
- **start_page.py**: Manages the start page of the survey, introducing participants to the study.
- **streamlit_app.py**: The main entry point for running the Streamlit app.
- **topic_questions.py**: Handles the page for topic-specific questions where participants evaluate political statements.
- **treatment.py**: Handles the logic for randomizing participants into different treatment groups (targeted, non-targeted, false-targeted).
- **treatment_eval.py**: Manages the treatment evaluation page, where participants assess whether the messages were targeted toward them.
- **README.md**
The documentation for the repository and instructions for running the web application and analyzing the data.
- **requirements.txt**
Lists the Python dependencies needed to run the Streamlit application, including OpenAI's API library and data processing tools.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adrianzarbock/microtargeting-llm.git
   cd microtargeting-llm
   ```

2. **Install required dependencies:**
   For the survey application:
   ```bash
   pip install -r survey_app/requirements.txt
   ```

   For data analysis:
   ```bash
   pip install -r analysis/requirements.txt
   ```

3. **Set up API keys:**
   - Add your OpenAI API key to `secrets.toml` in the `.streamlit/` directory to enable message generation.
    ```toml  
    DEVELOPMENT = true           # Set to true for local development, false for production
    EMAIL = ""                   # Email for display at start page

    OPENAI_API_KEY = ""          # Your OpenAI API key for generating political messages
    GOOGLE_SHEET_KEY = ""        # The unique key for the Google Sheet where participant responses are stored

    [GOOGLE_SHEET_CREDS]         # JSON credentials for accessing Google Sheets
    json_key = '''
    {
    // Paste your Google service account credentials here
    }
    '''
    ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run survey_app/streamlit_app.py
   ```

5. **Analyze survey data:**
   Open the Jupyter notebook in the `analysis/` folder to analyze the collected survey data:
   ```bash
   jupyter notebook analysis/data_analysis.ipynb
   ```