import streamlit as st
import time
from functions import write_to_google_sheet, scroll_to_top

def demographics(PAGE): # Demographics

    if 'successfully_written_page' + str(PAGE) not in st.session_state:
        st.session_state["successfully_written_page" + str(PAGE)] = False

    if 'input_disabled' + str(PAGE) not in st.session_state:
        st.session_state["input_disabled" + str(PAGE)] = False

    page_container = st.empty()
    with page_container.container():

        st.write("##### Zu Beginn möchten wir Sie bitten, einige Angaben zu Ihrer Person zu machen.")

        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()

        if 'age' not in st.session_state:
            if st.session_state.DEVELOPMENT:
                st.session_state.age = 18
            else:
                st.session_state.age = None

        if 'gender' not in st.session_state:
            if st.session_state.DEVELOPMENT:
                st.session_state.gender = "Männlich"
            else:
                st.session_state.gender = None

        if 'education' not in st.session_state:
            if st.session_state.DEVELOPMENT:
                st.session_state.education = "Hochschulabschluss"
            else:
                st.session_state.education = None

        age = st.number_input("Alter",
                                min_value=18,
                                max_value=150,
                                value=st.session_state.age if st.session_state.age else None,
                                disabled=st.session_state.input_disabled,
                                placeholder="Bitte geben Sie Ihr Alter ein.",
                                help="Bitte geben Sie Ihr Alter in Jahren an.")
        st.write("---")

        gender_options = ["Männlich", "Weiblich", "Divers", "Keine Angabe"]
        gender = st.radio("Geschlecht",
                            gender_options,
                            index=gender_options.index(st.session_state.gender) if st.session_state.gender else None,
                            disabled=st.session_state.input_disabled,
                            horizontal=False,
                            help="Bitte geben Sie an, welchem Geschlecht Sie sich zugehörig fühlen.")
        st.write("---")

        education_options = ["Kein Abschluss", "Hauptschulabschluss", "Realschulabschluss", "Abitur", "Hochschulabschluss", "Keine Angabe"]
        education = st.radio("Höchster Bildungsabschluss",
                                education_options,
                                index=education_options.index(st.session_state.education) if st.session_state.education else None,
                                disabled=st.session_state.input_disabled,
                                horizontal=False,
                                help="Bitte geben Sie Ihren höchsten Bildungsabschluss an.")

        st.write("---")

        if 'politics' not in st.session_state:
            if st.session_state.DEVELOPMENT:
                st.session_state.politics = "stark"
            else:
                st.session_state.politics = None
                
        politics_options = ["Sehr stark",
                            "stark",
                            "mittelmäßig",
                            "weniger stark",
                            "überhaupt nicht"]

        politics = st.radio("Wie stark interessieren Sie sich im Allgemeinen für Politik?",
                            politics_options,
                            index=politics_options.index(st.session_state.politics) if st.session_state.politics else None,
                            disabled=st.session_state.input_disabled,
                            horizontal=False,
                            help="Bitte geben Sie an, wie stark Sie sich für Politik interessieren.")
    
    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()
    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()

    if next_button_placeholder.button("Weiter"):
        if not all([age, gender, education, politics]):
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            st.session_state["current_page"] = PAGE + 1
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()

            st.session_state["input_disabled" + str(PAGE)] = True
            
            if not st.session_state["successfully_written_page" + str(PAGE)]:
                write_to_google_sheet("Demographics", st.session_state.participant_id, st.session_state.start_time, time.time(), age, gender, education, politics)
                st.session_state["successfully_written_page" + str(PAGE)] = True
            st.session_state.pop("start_time")

            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.education = education
            st.session_state.politics = politics
            
            scroll_to_top()
            st.rerun()