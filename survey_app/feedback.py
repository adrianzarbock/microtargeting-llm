import streamlit as st
import time
from functions import scroll_to_top, write_to_google_sheet

def feedback(PAGE):

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    page_container = st.empty()
    with page_container.container():
        
        st.write("""##### Informationen zum tatsächlichen Hintergrund der Studie

In dieser Studie untersuchen wir, ob und inwiefern große generative Sprachmodelle (wie z.B. *ChatGPT*) in der Lage sind, zielgerichtete politische Botschaften zu generieren, die eine höhere Überzeugungskraft besitzen als nicht zielgerichtete Botschaften. 

Um diese Frage zu beantworten, haben wir Sie gebeten, einige Angaben zu Ihrer Person, Ihren politischen Überzeugungen und Ihrer Meinung zu verschiedenen politischen Themen zu machen. Anschließend wurden Ihnen Botschaften zu diesen Themen präsentiert, die jeweils entgegengesetzte Positionen vertreten. Je nachdem, welcher Gruppe Sie zufällig zugeordnet wurden, wurden Ihnen entweder zielgerichtete oder nicht zielgerichtete Botschaften gezeigt. In jedem Fall wurden diese Botschaften jedoch von einem generativen Sprachmodell erstellt. 

Nachdem Sie die einzelnen Botschaften gelesen haben, wurde erhoben, wie überzeugend Sie diese wahrgenommen haben. Dies dient dazu, die Überzeugungskraft der Botschaften zu messen und damit die zentrale Fragestellung der Studie zu beantworten.

**Bitte beachten Sie: Alle Botschaften, die Sie gesehen haben, wurden von einem generativen Sprachmodell erstellt und stammen nicht von echten Personen. Sie sollen daher nicht als Meinungen realer Personen interpretiert werden. In den Botschaften präsentierte Fakten und Argumente sind nicht notwendigerweise korrekt oder wahr.**

Wir bitten um Ihr Verständnis, dass wir Ihnen diese Informationen erst jetzt mitteilen konnten. Dies ist notwendig, um Ihre unverfälschte Reaktion auf die Botschaften zu erhalten.
""")
        st.write("---")
        st.write("##### Feedback")
        st.write('Falls Sie der Studienleitung etwas bezüglich der Studie mitteilen möchten, dann können Sie dies in dem angelegten Textfeld tun. Klicken Sie anschließend oder wenn Sie nichts mitteilen möchten, auf „Weiter“.')
        feedback = st.text_area("Feedback", height=100)

    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()

    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()

    if next_button_placeholder.button("Weiter"):
        if False:
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            st.session_state.feedback = feedback
            st.session_state["current_page"] = PAGE + 1
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()
            write_to_google_sheet("Feedback", st.session_state.participant_id, st.session_state.start_time, time.time(), st.session_state.feedback)
            st.session_state.pop("start_time")
            scroll_to_top()
            
            st.rerun()