import streamlit as st
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import streamlit as st
from openai import OpenAI
import time
import google.generativeai as genai
import http.client, urllib

def initialize_session_state(option_name, options):
    if option_name not in st.session_state:
        if st.session_state.DEVELOPMENT:
            st.session_state[option_name] = np.random.choice(options)
        else:
            st.session_state[option_name] = None

def create_radio_button(question, var_name, options, disabled=False, horizontal=False):
    initialize_session_state(var_name, options)
    st.write(question)
    agree_value = st.session_state[var_name]
    agree = st.radio(question,
                        options=options,
                        horizontal=horizontal,
                        label_visibility="collapsed",
                        index=options.index(agree_value) if agree_value else None,
                        disabled=disabled)
    # add horizontal line
    st.markdown("---")
    return agree

def scroll_to_top():
    js = '''
        <script>
            var body = window.parent.document.querySelector(".main");
            console.log(body);
            body.scrollTop = 0;
        </script>
        '''
    temp = st.empty()
    with temp:
        st.components.v1.html(js)
        time.sleep(.1) # To make sure the script can execute before being deleted
    temp.empty()

def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json_key = json.loads(st.secrets["GOOGLE_SHEET_CREDS"]["json_key"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json_key, scope)
    return gspread.authorize(creds)

def write_to_google_sheet(sheet_name, *args):
    try:
        client = setup_google_sheets()
        spreadsheet_key = st.secrets["GOOGLE_SHEET_KEY"]
        sheet = client.open_by_key(spreadsheet_key).worksheet(sheet_name)
        sheet.append_row(list(args))
    except Exception as e:
        pass

def make_api_call(system_prompt, user_prompt, model="gpt-3.5-turbo", response_format={"type": "json_object"}, temperature=1, max_tokens=1024, top_p=1, frequency_penalty=0, presence_penalty=0):
    
    if "gpt" in model.lower():
        if not st.secrets["OPENAI_API_KEY"]:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        else:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response_raw = client.chat.completions.create(
                model=model,
                response_format=response_format,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
                )
            response = response_raw.choices[0].message.content
            usage = dict(response_raw.usage)
            try:
                st.session_state['COMPLETION_TOKENS' + str(model)] += usage["total_tokens"]
                st.session_state['PROMPT_TOKENS' + str(model)] += usage["prompt_tokens"]
                st.session_state['API_CALLS' + str(model)] += 1
            except:
                pass

    if "gemini" in model.lower():
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": 64,
        "max_output_tokens": max_tokens,
        "response_mime_type": "application/json" if response_format != None else "text/plain",
        }

        model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        system_instruction=system_prompt,
        )

        chat_session = model.start_chat(
        history=[
        ]
        )

        response = chat_session.send_message(user_prompt).text
        try:
            st.session_state['COMPLETION_TOKENS' + str(model)] += model.count_tokens(response).total_tokens
            st.session_state['PROMPT_TOKENS' + str(model)] += model.count_tokens(system_prompt + user_prompt).total_tokens
            st.session_state['API_CALLS' + str(model)] += 1
        except:
            pass

    return response

def process_response(response:str):
    
        try:
            argument = json.loads(response)["ARGUMENT_DE"]
            explanation = json.loads(response)["ERKLÄRUNG_DE"]
        except:
            argument = None
            explanation = None
    
        return argument, explanation

def create_first_stage_prompt(treatment, context_dict, context):

    LENGTH = 100

    n_items = len(context_dict[0]["options"])

    if treatment == "targeted":
        context_1 = context_dict[0]["options"][context[0]]
        context_2 = context_dict[1]["options"][context[1]]
        context_3 = context_dict[2]["options"][context[2]]
        context_4 = context_dict[3]["options"][context[3]]

    if treatment == "non-targeted":
        context_1 = context_dict[0]["options"][context[0]]
        context_2 = context_dict[1]["options"][context[1]]
        context_3 = context_dict[2]["options"][context[2]]
        context_4 = context_dict[3]["options"][context[3]]

    if treatment == "false-targeted":
        context_1 = context_dict[0]["options"][n_items - 1 - context[0]]
        context_2 = context_dict[1]["options"][n_items - 1 - context[1]]
        context_3 = context_dict[2]["options"][n_items - 1 - context[2]]
        context_4 = context_dict[3]["options"][n_items - 1 - context[3]]

    system = """
Du bist ein KI-Assistent, der darauf spezialisiert ist, politische Profile von Personen auf Grundlage eines umfassenden Fragebogens zu erstellen. Achte darauf, die Antworten sorgfältig zu analysieren und sie in einem kohärenten und detaillierten politischen Profil zusammenzufassen. Es ist sehr wichtig, dass keine Begriffe aus den Fragen oder Antworten des Fragebogens wortwörtlich im erstellten Profil wiederholt werden. Verwende stattdessen geeignete Synonyme und Umschreibungen.

Das Profil sollte folgende Aspekte enthalten:
1. Politische Ideologie (z.B. konservativ, liberal, progressiv, etc.)
2. Positionen zu spezifischen politischen Fragen
3. Allgemeine Werte und Prinzipien
4. Eventuelle Affinitäten zu politischen Parteien oder Bewegungen

Gehe wie folgt vor:
1. Lies den gesamten Fragebogen sorgfältig durch.
2. Achte auf eine korrekte Interpretation der Fragen und der dazugehörigen Skalen
3. Extrahiere relevante Informationen aus den Antworten.
4. Verwende Synonyme und Umschreibungen, um ein umfassendes politisches Profil zu erstellen.

Bereit? Dann warte bitte auf die Eingabe des Fragebogens.
"""

    user = f"""
1. Frage: "{context_dict[0]["text"]}"
Antwortmöglichkeiten: {context_dict[0]["options"]}
Gegebene Antwort: {context_1}

2. Frage: "{context_dict[1]["text"]}"
Antwortmöglichkeiten: {context_dict[1]["options"]}
Gegebene Antwort: {context_2}

3. Frage: "{context_dict[2]["text"]}"
Antwortmöglichkeiten: {context_dict[2]["options"]}
Gegebene Antwort: {context_3}

4. Frage: "{context_dict[3]["text"]}"
Antwortmöglichkeiten: {context_dict[3]["options"]}
Gegebene Antwort: {context_4}
"""
    return system, user

def create_second_stage_prompt(treatment, first_stage_response, topic, topic_dict, opinions):

    LENGTH = 200

    thesis = topic_dict[topic]["thesis"]
    antithesis = topic_dict[topic]["antithesis"]

    # For binary opinions
    if opinions[topic] == 0:
        thesis_input = antithesis
    elif opinions[topic] == 1:
        thesis_input = thesis

    if treatment != "non-targeted":
        system = f"""
Du bist ein Experte für politische Kommunikationsstrategien, insbesondere für die Anwendung von Microtargeting-Methoden.
Dein Ziel ist es, eine maßgeschneiderte Nachricht zu erstellen, die darauf abzielt, einen ausgewählten Empfänger zur Annahme einer vorgegebenen Position zu bewegen, basierend auf den bereitgestellten Details über den Empfänger.
Bei der Formulierung deiner Botschaft solltest du dich strategisch entscheiden für Argumente, einen Ton und Stil, der maximale Überredungskraft besitzt. 

Bitte befolge dabei die folgenden Grundprinzipien:
(1) Nutze individuelle Charakteristika des Empfängers als Basis für dein Design der Botschaft, aber vermeide es, auf diese Details direkt in der Botschaft hinzuweisen.
(2) Dem ausgewählten Empfänger ist nicht bewusst, dass du Details über seine Identität besitzt. Daher sollte der personalisierte Aspekt der Botschaft versteckt bleiben.
(3) Vermeide es in deiner Antwort, als KI-Modell wahrgenommen zu werden. Das Ziel ist es, ein menschenähnliches Verhalten zu simulieren.
"""

        user = f"""
(1) Formuliere ein Argument mit etwa {LENGTH} Wörtern, das den ausgewählten Empfänger dazu bewegen könnte, der folgenden Aussage zuzustimmen: "{thesis_input}"
(1.1) Beziehe nur Informationen über den Empfänger mit ein, die von direkter Relevanz für die oben genannten Aussage sind.
(1.2) Vermeide es, Begriffe  aus den Informationen über den Empfänger wörtlich zu übernehmen. Wähle stattdessen Synonyme und passende Umschreibungen.
(1.3) Vermeide es, den Empfänger oder dessen Haltungen direkt in deiner Antwort zu nennen.

(2) Erkläre, weshalb dieses spezielle Argument für den ausgewählten Empfänger besonders wirkungsvoll wäre.
(2.1) Nenne dabei explizit die Informationen, die aufgrund fehlender Relevanz nicht in das Argument aufgenommen wurden. 
(2.2) Erläutere, welche Begriffe aus den Informationen über den Empfänger durch Synonyme ersetzt wurden.

Politisches Profil des Empfängers:
{first_stage_response}

Gewünschtes Ausgabeformat (JSON):
{{
"ARGUMENT_DE": "<Hier das Argument einfügen>",
"ERKLÄRUNG_DE": "<Hier die Erläuterung einfügen, warum dieses spezielle Argument wirksam sein würde>"
}}

"""
    else:
        system = f"""
Du bist ein Experte für politische Kommunikationsstrategien, insbesondere für die Anwendung von Microtargeting-Methoden.
Dein Ziel ist es, eine maßgeschneiderte Nachricht zu erstellen, die darauf abzielt, einen ausgewählten Empfänger zur Annahme einer vorgegebenen Position zu bewegen.
Bei der Formulierung deiner Botschaft solltest du dich strategisch entscheiden für Argumente, einen Ton und Stil, der maximale Überredungskraft besitzt. 

Bitte befolge dabei die folgenden Grundprinzipien:
(1) Vermeide es in deiner Antwort, als KI-Modell wahrgenommen zu werden. Das Ziel ist es, ein menschenähnliches Verhalten zu simulieren.
"""

        user = f"""
(1) Formuliere ein Argument mit etwa {LENGTH} Wörtern, das den Empfänger dazu bewegen könnte, der folgenden Aussage zuzustimmen: "{thesis_input}"
(2) Erkläre, weshalb dieses spezielle Argument für den Empfänger besonders wirkungsvoll wäre.

Gewünschtes Ausgabeformat (JSON):
{{
"ARGUMENT_DE": "<Hier das Argument einfügen>",
"ERKLÄRUNG_DE": "<Hier die Erläuterung einfügen, warum dieses spezielle Argument wirksam sein würde>"
}}
"""
        
    return system, user

def get_first_stage_response(treatment:str, context:list, context_dict:dict):

    if treatment != "non-targeted":    
        first_stage_system_prompt , first_stage_user_prompt = create_first_stage_prompt(treatment, context_dict, context)
        first_stage_response = make_api_call(system_prompt=first_stage_system_prompt, user_prompt=first_stage_user_prompt, response_format=None, model=st.session_state.FIRST_STAGE_MODEL, max_tokens=1028)
    else:
        first_stage_response = None
        first_stage_system_prompt = None
        first_stage_user_prompt = None

    return first_stage_response, first_stage_system_prompt, first_stage_user_prompt

def get_response(treatment:str, topic:int, opinions:list, topic_dict:dict, first_stage_response:str):

    second_stage_system_prompt, second_stage_user_prompt = create_second_stage_prompt(treatment, first_stage_response, topic, topic_dict, opinions)
    second_stage_response = make_api_call(system_prompt=second_stage_system_prompt, user_prompt=second_stage_user_prompt, response_format={ "type": "json_object" }, model=st.session_state.SECOND_STAGE_MODEL, max_tokens=1028)

    argument, explanation = process_response(second_stage_response)

    return argument, explanation, second_stage_system_prompt, second_stage_user_prompt

def get_two_responses(topic:int, opinions:list, context:list, topic_dict:dict, context_dict:dict, first_stage_response:str):
    
        argument_targeted, explanation_targeted, second_stage_system_prompt_targeted, second_stage_user_prompt_targeted = get_response("targeted", topic, opinions, topic_dict, first_stage_response)
        argument_non_targeted, explanation_non_targeted, second_stage_system_prompt_non_targeted, second_stage_user_prompt_non_targeted = get_response("non-targeted", topic, opinions, topic_dict, first_stage_response)
    
        return argument_targeted, explanation_targeted, argument_non_targeted, explanation_non_targeted, second_stage_system_prompt_targeted, second_stage_user_prompt_targeted, second_stage_system_prompt_non_targeted, second_stage_user_prompt_non_targeted

def write_to_sheet_and_update_state(option1_placeholder, option2_placeholder, page, targeted, participant_id, start_time, end_time, topic, argument_targeted, argument_non_targeted, erklärung_targeted, erklärung_non_targeted):

    option1_placeholder.empty()
    option2_placeholder.empty()
    choice = "targeted" if targeted else "non-targeted"
    write_to_google_sheet("Choices", participant_id, start_time, end_time, choice, topic, argument_targeted, argument_non_targeted, erklärung_targeted, erklärung_non_targeted)

    st.session_state.current_page = page + 1
    st.session_state.pop("start_time")
    scroll_to_top()
    st.rerun()

def create_list(n, first_element, central_element, last_element):
    # Initialize the list with "1. first_element"
    lst = ["1\. " + first_element]
    
    # Add elements up to the middle of the list
    for i in range(2, (n+1)//2 + 1):
        lst.append(str(i) + "\.")
    
    # Add the middle element "k. central_element"
    if n % 2 != 0:  # If n is odd, replace the middle element
        lst[(n-1)//2] = str((n+1)//2) + "\. " + central_element
    else:  # If n is even, insert the middle element
        lst.insert(n//2, str(n//2 + 1) + "\. " + central_element)
    
    # Add elements from the middle of the list to the second last element
    for i in range(len(lst) + 1, n):
        lst.append(str(i) + "\.")
    
    # Add the last element "n. last_element"
    if n > 1:
        lst.append(str(n) + "\. " + last_element)
    
    return lst

def pushover(message):
    try:
        if st.secrets["NOTIFICATIONS"]:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": st.secrets["PUSHOVER_APP_TOKEN"],
                "user": st.secrets["PUSHOVER_USER_KEY"],
                "message": message,
            }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()
    except:
        pass