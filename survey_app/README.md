## Overview

This project is a Streamlit-based web application designed to study the perception of political messages. Participants are guided through a series of pages where they provide demographic information, read political messages, and evaluate their persuasiveness. The application uses OpenAI's GPT models models to generate and process responses.

## Project Structure

```
.gitignore
.streamlit/
	config.toml
	secrets.toml
closing_page.py
config.py
constants.py
demographics.py
dimensions.py
feedback.py
functions.py
introduction.txt
page_template.py
README.md
requirements.txt
start_page.py
streamlit_app.py
topic_questions.py
treatment_eval.py
treatment.py
```

## Key Files and Directories

- **.streamlit**: Contains configuration files for Streamlit.
- **closing_page.py**: Handles the closing page of the study.
- **config.py**: Contains the [`setup_page_config`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fadrianzarbock%2Fopenai_project%2Fconfig.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A2%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fadrianzarbock%2Fopenai_project%2Fstreamlit_app.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A12%2C%22character%22%3A19%7D%7D%5D%2C%22d0467efb-9e67-4357-b3dd-23844c4482b7%22%5D "Go to definition") function to configure the Streamlit page.
- **constants.py**: Stores constants used throughout the application.
- **demographics.py**: Handles the demographics page.
- **dimensions.py**: Handles the dimensions page.
- **feedback.py**: Handles the feedback page.
- **functions.py**: Contains utility functions such as [`make_api_call`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fadrianzarbock%2Fopenai_project%2Ffunctions.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A61%2C%22character%22%3A4%7D%7D%5D%2C%22d0467efb-9e67-4357-b3dd-23844c4482b7%22%5D "Go to definition"), [`write_to_google_sheet`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fadrianzarbock%2Fopenai_project%2Ffunctions.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A52%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fadrianzarbock%2Fopenai_project%2Fstart_page.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A22%7D%7D%5D%2C%22d0467efb-9e67-4357-b3dd-23844c4482b7%22%5D "Go to definition"), and more.
- **introduction.txt**: Contains the introduction text displayed on the start page.
- **page_template.py**: Template for creating new pages.
- **start_page.py**: Handles the start page of the study.
- **streamlit_app.py**: Main entry point for the Streamlit application.
- **topic_questions.py**: Handles the topic questions page.
- **treatment_eval.py**: Handles the treatment evaluation page.
- **treatment.py**: Handles the treatment page.

## Setup

### Prerequisites

- Python 3.7 or higher
- Streamlit
- OpenAI API key
- Google Sheets API credentials

### Installation

1. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

2. Set up the 

secrets.toml

 file with your API keys and other secrets:
    ```toml
    [secrets]
    OPENAI_API_KEY = "your-openai-api-key"
    GEMINI_API_KEY = "your-gemini-api-key"
    GOOGLE_SHEET_CREDS = { json_key = "your-google-sheets-json-key" }
    GOOGLE_SHEET_KEY = "your-google-sheet-key"
    EMAIL = "your-email"
    DEVELOPMENT = true
    ```

## Running the Application

To run the application, use the following command:
```sh
streamlit run streamlit_app.py
```