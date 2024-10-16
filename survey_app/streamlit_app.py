import streamlit as st
import numpy as np

from start_page import start_page
from demographics import demographics
from dimensions import dimensions
from closing_page import closing_page
from feedback import feedback
from topic_questions import topic_questions
from treatment import treatment
from treatment_eval import treatment_eval

from config import setup_page_config
import constants

st.session_state.DEVELOPMENT = st.secrets["DEVELOPMENT"]

# Set up OpenAI API key from secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

if 'FIRST_STAGE_MODEL' not in st.session_state:
    st.session_state.FIRST_STAGE_MODEL = "gpt-4o"

if 'SECOND_STAGE_MODEL' not in st.session_state:
    st.session_state.SECOND_STAGE_MODEL = "gpt-4o"

if 'COMPLETION_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL) not in st.session_state:
    st.session_state['COMPLETION_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL)] = 0

if 'COMPLETION_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL) not in st.session_state:
    st.session_state['COMPLETION_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL)] = 0

if 'PROMPT_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL) not in st.session_state:
    st.session_state['PROMPT_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL)] = 0

if 'PROMPT_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL) not in st.session_state:
    st.session_state['PROMPT_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL)] = 0

if 'API_CALLS' + str(st.session_state.FIRST_STAGE_MODEL) not in st.session_state:
    st.session_state['API_CALLS' + str(st.session_state.FIRST_STAGE_MODEL)] = 0

if 'API_CALLS' + str(st.session_state.SECOND_STAGE_MODEL) not in st.session_state:
    st.session_state['API_CALLS' + str(st.session_state.SECOND_STAGE_MODEL)] = 0

# SET TREATMENT
if 'treatment' not in st.session_state:
    st.session_state.treatment = np.random.choice(["targeted", "non-targeted", "false-targeted"])

# SET TOPICS ORDER
if 'topics_order' not in st.session_state:
    topics_order = [0, 1, 2, 3]
    np.random.shuffle(topics_order)
    st.session_state.topics_order = topics_order

# Load topic dictionary
st.session_state.topic_dict = constants.topic_dict()

# Load context dictionary
st.session_state.context_dict = constants.context_dict()

# Load agree options
st.session_state.agree_options = constants.agree_options()

# Load binary options
st.session_state.binary_options = constants.binary_options()

# set page header
st.session_state.page_header = 'Studie zur Wahrnehmung politischer Botschaften'
if st.session_state.DEVELOPMENT:
    st.session_state.page_header = st.session_state.page_header + '\n\n ---'
    st.session_state.page_header = st.session_state.page_header + '\n\n**:black[ENTWICKLUNGSANSICHT:]**\n\n**TREATMENT:** *{}*, **TOPIC ORDER:** *{}*'.format(st.session_state.treatment, st.session_state.topics_order)
    st.session_state.page_header = st.session_state.page_header + '\n\n **MODEL:** *{}*, **INPUT TOKENS:** *{}*, **OUTPUT TOKENS:** *{}*, **TOTAL TOKENS:** *{}*, **# API CALLS** *{}*'.format(st.session_state.FIRST_STAGE_MODEL, st.session_state['PROMPT_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL)], st.session_state['COMPLETION_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL)], st.session_state['PROMPT_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL)] + st.session_state['COMPLETION_TOKENS' + str(st.session_state.FIRST_STAGE_MODEL)], st.session_state['API_CALLS' + str(st.session_state.FIRST_STAGE_MODEL)])
    if st.session_state.FIRST_STAGE_MODEL != st.session_state.SECOND_STAGE_MODEL:
        st.session_state.page_header = st.session_state.page_header + '\n\n **MODEL:** *{}*, **INPUT TOKENS:** *{}*, **OUTPUT TOKENS:** *{}*, **TOTAL TOKENS:** *{}*, **# API CALLS** *{}*'.format(st.session_state.SECOND_STAGE_MODEL, st.session_state['PROMPT_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL)], st.session_state['COMPLETION_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL)], st.session_state['PROMPT_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL)] + st.session_state['COMPLETION_TOKENS' + str(st.session_state.SECOND_STAGE_MODEL)], st.session_state['API_CALLS' + str(st.session_state.SECOND_STAGE_MODEL)])
    st.session_state.page_header = st.session_state.page_header + '\n\n ---'
def main():
    
    # Set up Streamlit page config
    setup_page_config()

    st.subheader(st.session_state.page_header)
    st.write("")
    pages = [start_page, demographics, dimensions, topic_questions, treatment, treatment, treatment, treatment, treatment_eval, feedback, closing_page]

    current_page = st.session_state.get("current_page", 0)

    st.progress(current_page / (len(pages) - 1), text=f"{(current_page)/(len(pages)-1) * 100:.0f}% abgeschlossen")
    st.write("")
    
    placeholder = st.empty()
    pages[current_page](PAGE=current_page)
    placeholder.text("")

if __name__ == "__main__":
    main()
