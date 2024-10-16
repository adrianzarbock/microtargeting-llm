import streamlit as st
import time
from functions import (
    write_to_google_sheet,
    scroll_to_top,
    get_response,
    create_radio_button,
)


def treatment(PAGE):

    TOPIC = int((PAGE) - 4)

    if "input_disabled_page" + str(PAGE) not in st.session_state:
        st.session_state["input_disabled_page" + str(PAGE)] = False

    if "successfully_written_page" + str(PAGE) not in st.session_state:
        st.session_state["successfully_written_page" + str(PAGE)] = False

    page_container = st.empty()
    with page_container.container():

        st.write(
            "Nachfolgend sehen Sie ein Argument zum Thema **"
            + st.session_state.topic_dict[st.session_state.topics_order[TOPIC]]["title"]
            + "**."
        )
        st.write(
            "**Bitte lesen Sie den folgenden Text sorgfältig durch bevor Sie mit der Umfrage fortfahren.**"
        )

        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()

        tile = st.container(border=True)

        with tile:
            st.write(
                st.session_state[
                    "argument_text" + str(st.session_state.topics_order[TOPIC])
                ]
            )

        with st.spinner("Bitte lesen Sie den Text sorgfältig durch."):
            try:
                NEXT_TOPIC = st.session_state.topics_order[TOPIC + 1]
                if "TOPIC_STATE" + str(NEXT_TOPIC) not in st.session_state:
                    (
                        st.session_state["argument_text" + str(NEXT_TOPIC)],
                        st.session_state["erklärung_text" + str(NEXT_TOPIC)],
                        st.session_state[
                            "second_stage_system_prompt" + str(NEXT_TOPIC)
                        ],
                        st.session_state["second_stage_user_prompt" + str(NEXT_TOPIC)],
                    ) = get_response(
                        treatment=st.session_state.treatment,
                        topic=NEXT_TOPIC,
                        opinions=st.session_state.opinions,
                        topic_dict=st.session_state.topic_dict,
                        first_stage_response=st.session_state.first_stage_response,
                    )
                    st.session_state["TOPIC_STATE" + str(NEXT_TOPIC)] = True
            except:
                NEXT_TOPIC = None
                st.session_state["ATTENTION_CHECK"] = True
                if "TOPIC_STATE" + str(NEXT_TOPIC) not in st.session_state:
                    st.session_state["TOPIC_STATE" + str(NEXT_TOPIC)] = True
                    time.sleep(10)

        st.write("---")
        st.write(" ")
        st.write(
            "**Nachdem Sie das Argument gelesen haben, möchten wir Sie nun bitten, einige Fragen dazu zu beantworten.**"
        )
        st.write("---")

        st.write("**Inwiefern stimmen Sie der folgenden Aussage zu?**")
        agree12 = create_radio_button(
            question="Das Argument ist gut begründet." + " " * PAGE,
            var_name=str("agree12_page" + str(PAGE)),
            options=st.session_state.agree_options,
            disabled=st.session_state[
                "input_disabled_page" + str(PAGE)
            ],
        )

        st.write("**Inwiefern stimmen Sie der folgenden Aussage zu?**")
        agree11 = create_radio_button(
            question=f'"*{st.session_state.topic_dict[st.session_state.topics_order[TOPIC]]["thesis"]}*"',
            var_name=str("agree11_page" + str(PAGE)),
            options=st.session_state.agree_options,
            disabled=st.session_state[
                "input_disabled_page" + str(PAGE)
            ],
        )

    button_col1, button_col2 = st.columns(2)
    back_button_placeholder = button_col1.empty()
    next_button_placeholder = button_col2.empty()

    if back_button_placeholder.button("Zurück"):
        st.session_state["current_page"] = PAGE - 1
        scroll_to_top()
        st.rerun()
    if next_button_placeholder.button("Weiter"):
        if not all([agree11, agree12]):
            st.error("Bitte beantworten Sie alle Fragen.")
        else:
            back_button_placeholder.empty()
            next_button_placeholder.empty()
            page_container.empty()
            scroll_to_top()

            st.session_state["input_disabled_page" + str(PAGE)] = True

            st.session_state["agree11_page" + str(PAGE)] = agree11
            st.session_state["agree12_page" + str(PAGE)] = agree12

            if not st.session_state[
                "successfully_written_page"
                + str(PAGE)
            ]:
                write_to_google_sheet(
                    "Treatment",
                    st.session_state.participant_id,
                    st.session_state.start_time,
                    time.time(),
                    st.session_state.treatment,
                    st.session_state.topic_dict[st.session_state.topics_order[TOPIC]]["title"],
                    st.session_state[
                        "argument_text" + str(st.session_state.topics_order[TOPIC])
                    ],
                    st.session_state[
                        "erklärung_text" + str(st.session_state.topics_order[TOPIC])
                    ],
                    st.session_state[
                        "second_stage_system_prompt"
                        + str(st.session_state.topics_order[TOPIC])
                    ],
                    st.session_state[
                        "second_stage_user_prompt"
                        + str(st.session_state.topics_order[TOPIC])
                    ],
                    agree11,
                    agree12,
                )

                st.session_state[
                    "successfully_written_page"
                    + str(PAGE)
                ] = True

            st.session_state.pop("start_time")
            st.session_state["current_page"] = PAGE + 1
            st.rerun()

    if st.session_state.DEVELOPMENT:
        if st.checkbox("Debug Info anzeigen"):
            st.subheader("Treatment")
            st.write(st.session_state.treatment)
            st.subheader("Erklärung")
            st.write(st.session_state["erklärung_text" +str(st.session_state.topics_order[TOPIC])])
            st.subheader("First Stage System Prompt")
            st.code(st.session_state.first_stage_system_prompt)
            st.subheader("First Stage User Prompt")
            st.code(st.session_state.first_stage_user_prompt)
            st.subheader("Second Stage System Prompt")
            st.code(st.session_state["second_stage_system_prompt" + str(st.session_state.topics_order[TOPIC])])
            st.subheader("Second Stage User Prompt")
            st.code(st.session_state["second_stage_user_prompt" + str(st.session_state.topics_order[TOPIC])])
