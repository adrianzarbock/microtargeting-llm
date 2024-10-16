import streamlit as st
import time
import numpy as np
from functions import (
    write_to_google_sheet,
    create_radio_button,
    scroll_to_top,
    create_list,
    pushover,
)


def treatment_eval(PAGE):

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    if "input_disabled_page" + str(PAGE) not in st.session_state:
        st.session_state["input_disabled_page" + str(PAGE)] = False

    if "successfully_written_page" + str(PAGE) not in st.session_state:
        st.session_state["successfully_written_page" + str(PAGE)] = False

    page_container = st.empty()
    with page_container.container():

        st.write(
            "##### Nachdem Sie sich mit den Argumenten auseinandergesetzt haben, möchten wir Sie bitten, die folgenden Fragen zu beantworten."
        )

        st.write("---")

        perceived_targeting = create_radio_button(
            "Wen würden die zuvor präsentierten Argumente Ihrer Meinung nach am ehesten überzeugen?",
            "perceived_targeting",
            create_list(
                    9,
                    "Jemand, der Ihnen sehr ähnlich ist (z. B. dieselben demografischen Merkmale und politischen Einstellungen)",
                    "ein allgemeines Publikum",
                    "Jemand, der sich sehr von Ihnen unterscheidet (z. B. gegensätzliche demografische Merkmale und politische Einstellungen)",
                ),
            st.session_state["input_disabled_page" + str(PAGE)],
        )

        attention_check = create_radio_button(
            "Um sicherzustellen, dass Sie die Fragen aufmerksam lesen, wählen Sie bitte 'Stimme voll und ganz zu'. Dies soll eine hohe Qualität der Daten gewährleisten.",
            "attention_check",
            st.session_state.agree_options,
            st.session_state["input_disabled_page" + str(PAGE)],
        )

    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()

    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()
    if next_button_placeholder.button("Weiter"):
        if not all([perceived_targeting, attention_check]):
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()
            scroll_to_top()

            st.session_state["input_disabled_page" + str(PAGE)] = True

            st.session_state.perceived_targeting = perceived_targeting
            st.session_state.attention_check = attention_check

            if not st.session_state["successfully_written_page" + str(PAGE)]:
                with st.spinner("Antworten werden gespeichert..."):
                    # write to google sheet
                    write_to_google_sheet(
                        "Post-Treatment",
                        st.session_state.participant_id,
                        st.session_state.start_time,
                        time.time(),
                        st.session_state.treatment,
                        perceived_targeting,
                        attention_check,
                    )
                    st.session_state["successfully_written_page" + str(PAGE)] = True

                    pushover("Ein Teilnehmer hat die Umfrage abgeschlossen.")

            st.session_state.pop("start_time")
            st.session_state["current_page"] = PAGE + 1
            st.rerun()
