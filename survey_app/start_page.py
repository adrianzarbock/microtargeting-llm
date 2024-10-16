import streamlit as st
import time
import uuid
from functions import write_to_google_sheet, scroll_to_top, create_radio_button

def start_page(PAGE):

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
        st.session_state.overall_start_time = time.time()

    if 'input_disabled' + str(PAGE) not in st.session_state:
        st.session_state["input_disabled" + str(PAGE)] = False

    with open('introduction.txt', 'r') as f:
        introduction_text = f.read()

    page_container = st.empty()
    with page_container.container():

        st.write("""##### Teilnahmeinformationen

Vielen Dank, dass Sie an unserer Untersuchung zur Wahrnehmung politischer Botschaften teilnehmen. Ihre Teilnahme hilft uns, wichtige Einblicke in die Meinungsbildung und Überzeugungskraft politischer Kommunikation zu gewinnen.
                 
**Ziel der Studie**

Das Ziel dieser Studie ist es, zu verstehen, wie unterschiedlich formulierte politische Botschaften auf Menschen wirken und welche Faktoren ihre Überzeugungskraft beeinflussen.

**Ablauf und Dauer**

Der Ablauf der Studie ist ganz einfach und dauert etwa 5-10 Minuten:

1. **Fragen zu Ihrer Person:** Zunächst bitten wir Sie, einige kurze Angaben zu Ihrer Person und zu Ihren Ansichten zu machen.
2. **Lesen der Botschaften:** Anschließend werden Ihnen verschiedene politische Botschaften zu aktuellen Themen präsentiert.
3. **Bewertung der Botschaften:** Nach dem Lesen jeder Botschaft bewerten Sie, wie überzeugend Sie diese finden.
                 
Alle Ihre Antworten werden anonym erfasst und streng vertraulich behandelt.

Als Dankeschön für Ihre Teilnahme haben Sie nach Abschluss der Studie die Möglichkeit, an einer Verlosung von vier Gutscheinen im Wert von jeweils 15 € für eine große lokale Buchhandlung teilzunehmen.
""")
        
        st.write(" ")

        with st.expander("Vollständige Teilnahmebedingungen anzeigen"):
            st.write(introduction_text.format(st.secrets['EMAIL']))

        st.write(" ")

        if 'terms_and_conditions' not in st.session_state:
            if st.session_state.DEVELOPMENT:
                st.session_state.terms_and_conditions = "Zustimmen"
            else:
                st.session_state.terms_and_conditions = None

        if 'input_disabled' not in st.session_state:
            st.session_state.input_disabled = False

        terms_and_conditions_options = ["Zustimmen", "Nicht zustimmen"]
        terms_and_conditions = create_radio_button("Ich habe die Teilnahmebedingungen gelesen und stimme zu.",
                                            "terms_and_conditions",
                                            terms_and_conditions_options,
                                            disabled=st.session_state["input_disabled" + str(PAGE)])


    start_button_placeholder = st.empty()

    if start_button_placeholder.button("Studie starten"):
        if terms_and_conditions != "Zustimmen":
            st.error("Bitte stimmen Sie den Teilnahmebedingungen zu um mit der Studie fortzufahren.")
        else:
            st.session_state.terms_and_conditions = terms_and_conditions
            st.session_state["current_page"] = PAGE + 1
            start_button_placeholder.empty()
            page_container.empty()
            scroll_to_top()

            st.session_state["input_disabled" + str(PAGE)] = True

            if 'participant_id' not in st.session_state:
                st.session_state.participant_id = str(uuid.uuid4())
                write_to_google_sheet("Start", st.session_state.participant_id, st.session_state.start_time, st.session_state.treatment)
                st.session_state.pop("start_time")

            st.rerun()
