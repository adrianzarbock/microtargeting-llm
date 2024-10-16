import streamlit as st
import time
from functions import scroll_to_top, create_radio_button, get_response, write_to_google_sheet

def topic_questions(PAGE):

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    page_container = st.empty()

    with page_container.container():

        st.write("##### Nun geht es um Ihre Meinung zu konkreten politischen Themen.\n##### Bitte geben Sie an, ob Sie den folgenden Aussagen (eher) zustimmen oder (eher) nicht zustimmen.")

        st.write("---")

        st.write('**Aussage 1**')
        agree01 = create_radio_button('"' + st.session_state.topic_dict[0]["thesis"] + '"',
                                        "agree01",
                                        options=st.session_state.binary_options,
                                        disabled=st.session_state.input_disabled)
        
        st.write('**Aussage 2**')
        agree02 = create_radio_button('"' + st.session_state.topic_dict[1]["thesis"] + '"',
                                        "agree02",
                                        options=st.session_state.binary_options,
                                        disabled=st.session_state.input_disabled)
        st.write('**Aussage 3**')
        agree03 = create_radio_button('"' + st.session_state.topic_dict[2]["thesis"] + '"',
                                        "agree03",
                                        options=st.session_state.binary_options,
                                        disabled=st.session_state.input_disabled)
        st.write('**Aussage 4**')
        agree04 = create_radio_button('"' + st.session_state.topic_dict[3]["thesis"] + '"',
                                        "agree04",
                                        options=st.session_state.binary_options,
                                        disabled=st.session_state.input_disabled)

    # Set up navigation buttons
    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()

    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()

    if next_button_placeholder.button("Weiter"):
        if not all([agree01, agree02, agree03, agree04]):
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            st.session_state.input_disabled = True
            st.session_state.opinions = [st.session_state.binary_options.index(agree01), st.session_state.binary_options.index(agree02), st.session_state.binary_options.index(agree03), st.session_state.binary_options.index(agree04)]
            st.session_state.agree01 = agree01
            st.session_state.agree02 = agree02
            st.session_state.agree03 = agree03
            st.session_state.agree04 = agree04

            st.session_state["current_page"] = PAGE + 1
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()

            scroll_to_top()

            if "argument_text" not in st.session_state:
                with st.spinner("Lädt..."):
                    write_to_google_sheet("Opinions", st.session_state.participant_id, st.session_state.start_time, time.time(), st.session_state.agree01, st.session_state.agree02, st.session_state.agree03, st.session_state.agree04)
                    NEXT_TOPIC = st.session_state.topics_order[0]
                    if  'TOPIC_STATE' + str(NEXT_TOPIC) not in st.session_state:
                        st.session_state["argument_text" + str(NEXT_TOPIC)], st.session_state["erklärung_text" + str(NEXT_TOPIC)], st.session_state["second_stage_system_prompt" + str(NEXT_TOPIC)], st.session_state["second_stage_user_prompt" + str(NEXT_TOPIC)] = get_response(treatment=st.session_state.treatment, topic=NEXT_TOPIC, opinions=st.session_state.opinions, topic_dict=st.session_state.topic_dict, first_stage_response=st.session_state.first_stage_response)
                        st.session_state["TOPIC_STATE" + str(NEXT_TOPIC)] = True
            st.session_state.pop("start_time")
            
            st.rerun()