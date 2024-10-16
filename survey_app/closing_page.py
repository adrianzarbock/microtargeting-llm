import streamlit as st
import time
from functions import write_to_google_sheet

def closing_page(PAGE):
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.success("Sie haben die Studie erfolgreich abgeschlossen. Vielen Dank für Ihre Teilnahme!")

    if 'email_success' not in st.session_state:
        st.session_state.email_success = False
    
    if True:
        st.write("**Nachfolgend haben Sie die Möglichkeit, Ihre E-Mail-Adresse einzutragen, um an der Gewinnauslosung teilzunehmen und/oder nach Abschluss der Studie über die Ergebnisse informiert zu werden.**")
        st.write("Ihre E-Mail-Adresse wird getrennt von Ihren Antworten gespeichert und kann nicht mit Ihren Antworten in Verbindung gebracht werden. Unmittelbar nach der Gewinnauslosung/Veröffentlichung der Studienergebnisse werden alle E-Mail-Adressen gelöscht.")
        
        if 'email_disabled' not in st.session_state:
            st.session_state.email_disabled = False

        email = st.text_input("E-Mail-Adresse",
                              help="Bitte geben Sie Ihre E-Mail-Adresse ein.",
                              disabled=st.session_state.email_disabled)
        
        lottery = st.checkbox("Ich möchte an der Gewinnauslosung teilnehmen.",
                              disabled=st.session_state.email_disabled)
        study_results = st.checkbox("Ich möchte nach Abschluss der Studie über die Ergebnisse informiert werden.",
                                    disabled=st.session_state.email_disabled)
        
        if st.button("Absenden",
                    disabled=st.session_state.email_disabled):
            if "@" not in email or "." not in email:
                st.error("Bitte geben Sie eine gültige E-Mail-Adresse ein.")
            elif not any([lottery, study_results]):
                    st.error("Bitte wählen Sie mindestens eine Option aus.")
            else:
                st.session_state.email_disabled = True
                try:
                    with st.spinner("E-Mail-Adresse wird gespeichert..."):
                        total_time = st.session_state.start_time - st.session_state.overall_start_time
                        date = time.strftime("%d.%m.%Y")
                        write_to_google_sheet("Emails", date, email, lottery, study_results, total_time, st.session_state.attention_check)
                        st.session_state.email_success = True
                    st.success("Vielen Dank! Ihre E-Mail-Adresse wurde erfolgreich gesendet.")
                    st.rerun()
                except Exception as e:
                    st.error("E-Mail-Adresse konnte nicht gesendet werden")

        if st.session_state.email_success:
            st.success("Vielen Dank! Ihre E-Mail-Adresse wurde erfolgreich gesendet.")