import streamlit as st
import time
from functions import scroll_to_top

def page_template(PAGE):

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    page_container = st.empty()

    with page_container.container():

        # Insert page content here
        st.write("##### This is a template for a page.")

    # Set up navigation buttons
    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()

    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()

    if next_button_placeholder.button("Weiter"):
        # Define the conditions for moving to the next page
        if False:
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            st.session_state["current_page"] = PAGE + 1
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()

            # Delete the start_time key from the session state
            st.session_state.pop("start_time")
            scroll_to_top()
            
            # Perform any necessary calculations or data storage
            with st.spinner("Lädt..."):
                # Perform any necessary calculations or data storage
                time.sleep(3)

            st.rerun()