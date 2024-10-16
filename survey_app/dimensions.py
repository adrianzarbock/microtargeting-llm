import streamlit as st
import numpy as np
import time
from functions import create_radio_button, get_first_stage_response, write_to_google_sheet, scroll_to_top

def dimensions(PAGE): # Political Dimensions

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    if 'input_disabled_page' + str(PAGE) not in st.session_state:
        st.session_state["input_disabled_page" + str(PAGE)] = False

    if 'successfully_written_page' + str(PAGE) not in st.session_state:
        st.session_state["successfully_written_page" + str(PAGE)] = False

    page_container = st.empty()
    with page_container.container():
        

        st.write("##### Zunächst geht es um Ihre grundlegende Einschätzung zu verschiedenen politischen Fragen.\n ##### Bitte beanworten Sie die folgenden Fragen wahrheitsgemäß.")
        st.write("---")

        st.write('**Frage 1**')
        agree05 = create_radio_button(st.session_state.context_dict[0]["text"],
                                    "agree05",
                                    st.session_state.context_dict[0]["options"],
                                    st.session_state["input_disabled_page" + str(PAGE)])
        
        st.write('**Frage 2**')
        agree06 = create_radio_button(st.session_state.context_dict[1]["text"],
                                    "agree06",
                                    st.session_state.context_dict[1]["options"],
                                    st.session_state["input_disabled_page" + str(PAGE)])
        
        st.write('**Frage 3**')
        agree07 = create_radio_button(st.session_state.context_dict[2]["text"],
                                    "agree07",
                                    st.session_state.context_dict[2]["options"],
                                    st.session_state["input_disabled_page" + str(PAGE)])
        
        st.write('**Frage 4**')
        agree08 = create_radio_button(st.session_state.context_dict[3]["text"],
                                    "agree08",
                                    st.session_state.context_dict[3]["options"],
                                    st.session_state["input_disabled_page" + str(PAGE)])
        
    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()

    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()

    if next_button_placeholder.button("Weiter"):
        if not all([agree05, agree06, agree07, agree08]):
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            st.session_state["input_disabled_page" + str(PAGE)] = True
            st.session_state["current_page"] = PAGE + 1
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()

            st.session_state.context = [st.session_state.context_dict[0]["options"].index(agree05), st.session_state.context_dict[1]["options"].index(agree06), st.session_state.context_dict[2]["options"].index(agree07), st.session_state.context_dict[3]["options"].index(agree08)]
            st.session_state.agree05 = agree05
            st.session_state.agree06 = agree06
            st.session_state.agree07 = agree07
            st.session_state.agree08 = agree08

            if "first_stage_response" not in st.session_state:
                with st.spinner("Lädt..."):
                    st.session_state.first_stage_response, st.session_state.first_stage_system_prompt, st.session_state.first_stage_user_prompt = get_first_stage_response(treatment=st.session_state.treatment, context=st.session_state.context, context_dict=st.session_state.context_dict)

            if not st.session_state["successfully_written_page" + str(PAGE)]:
                write_to_google_sheet(
                    "Positions",
                    st.session_state.participant_id,
                    st.session_state.start_time,
                    time.time(),
                    st.session_state.treatment,
                    agree05,
                    agree06,
                    agree07,
                    agree08,
                    st.session_state.first_stage_system_prompt,
                    st.session_state.first_stage_user_prompt,
                    st.session_state.first_stage_response,
                )
                st.session_state["successfully_written_page" + str(PAGE)] = True

            st.session_state.pop("start_time")
            scroll_to_top()
            st.rerun()