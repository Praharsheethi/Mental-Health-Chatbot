import streamlit as st
import os
import json
import google.generativeai as genai
from config import Config
from sentiment import analyze_sentiment
from persona import get_personality_response 
TRIGGER_WORDS = ["depressed", "hopeless", "suicidal", "overwhelmed", "anxious", "panic", "stressed", "worthless", "hurt"]

# JSON file to store journal & gratitude entries
DATA_FILE = "journal_entries.json"

# ==========================
# Apply Dark/Light Mode CSS
# ==========================
def apply_css(dark_mode):
    css = Config.DARK_MODE_CSS if dark_mode else Config.LIGHT_MODE_CSS
    st.markdown(css, unsafe_allow_html=True)

# ==========================
# Initialize Session State
# ==========================
def initialize_session():
    if 'dark_mode' not in st.session_state:
        st.session_state['dark_mode'] = False
    if 'writing_journal' not in st.session_state:
        st.session_state['writing_journal'] = False
    if 'writing_gratitude' not in st.session_state:
        st.session_state['writing_gratitude'] = False

# ==========================
# Save Journal/Gratitude Entry
# ==========================
def save_entry_to_json(entry, entry_type):
    """
    Saves a journal or gratitude entry to a JSON file.
    :param entry: User input text.
    :param entry_type: "journal" or "gratitude".
    """
    if not os.path.exists(DATA_FILE):
        data = {"journal": [], "gratitude": []}
    else:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {"journal": [], "gratitude": []}

    # Append the new entry
    data[entry_type].append(entry)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# ==========================
# Retrieve Past Entries
# ==========================
def get_past_entries(entry_type):
    """
    Retrieves past journal or gratitude entries.
    :param entry_type: "journal" or "gratitude".
    :return: List of past entries.
    """
    if not os.path.exists(DATA_FILE):
        return ["No entries found. Start writing today!"]

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data.get(entry_type, ["No entries found."])
        except json.JSONDecodeError:
            return ["No entries found."]

# ==========================
# Select Gemini Model
# ==========================
def get_model_name(model_choice):
    if model_choice == "Gemini 1.5 Flash":
        return "gemini-1.5-flash-latest"
    elif model_choice == "Gemini 1.5 Pro":
        return "gemini-1.5-pro-latest"
    else:
        return "gemini-1.0-pro"
def detect_distress(user_input):
    """Check if user input contains distress-related words."""
    return any(word in user_input.lower() for word in TRIGGER_WORDS)

# ==========================
# Generate Chatbot Response
# ==========================
def get_chat_response(chat_session, user_input):
    """Generate chatbot response and trigger alerts if distress is detected."""
    
    sentiment = analyze_sentiment(user_input)
    selected_persona = st.session_state.get("selected_persona", "Supportive Friend")  # Default persona

    # Check for distress and set alert
    if detect_distress(user_input) or sentiment == "negative":
        st.session_state["show_alert"] = True

    # Don't respond if input came from the sidebar
    if st.session_state.get("sidebar_journaling", False) or st.session_state.get("sidebar_gratitude", False):
        return "", sentiment  

    # Journaling & gratitude modes
    if "journal" in user_input.lower():
        st.session_state['writing_journal'] = True
        return "Great! What would you like to write in your journal today? 😊", sentiment

    if st.session_state.get('writing_journal', False):
        save_entry_to_json(user_input, "journal")
        st.session_state['writing_journal'] = False  
        return "Your journal entry has been saved! ✨ Want to see past journal entries?", sentiment

    if "gratitude" in user_input.lower():
        st.session_state['writing_gratitude'] = True
        return "Wonderful! What are you grateful for today? 🙏", sentiment

    if st.session_state.get('writing_gratitude', False):
        save_entry_to_json(user_input, "gratitude")
        st.session_state['writing_gratitude'] = False  
        return "Your gratitude entry has been saved! 🙌 Want to see past gratitude entries?", sentiment

    # Retrieve past entries
    if "show my journal" in user_input.lower():
        past_journals = get_past_entries("journal")
        return "📖 Here are your past journal entries:\n\n" + "\n".join(past_journals), sentiment

    if "show my gratitude" in user_input.lower():
        past_gratitudes = get_past_entries("gratitude")
        return "🙏 Here are your past gratitude entries:\n\n" + "\n".join(past_gratitudes), sentiment

    # Adjust chatbot responses based on selected personality
    persona_response = get_personality_response(selected_persona, user_input)

    # Default Chatbot Response
    try:
        response = chat_session.send_message(user_input)
        if response and hasattr(response, "text"):
            return f"{persona_response}\n\n{response.text}", sentiment
        else:
            return "I'm sorry, I couldn't process that. Please try again.", sentiment
    except Exception as e:
        return f"Error: {str(e)}", sentiment




# ==========================
# Create Gemini Chat Session
# ==========================
def create_chat_session(api_key, model_name, temperature, top_p, top_k, max_output_tokens):
    os.environ["GEMINI_API_KEY"] = api_key
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        safety_settings=Config.SAFETY_SETTINGS,
        generation_config=generation_config,
    )

    return model.start_chat(history=[])

# ==========================
# Fetch Entries for UI
# ==========================
def get_journal_entries():
    return get_past_entries("journal")

def get_gratitude_entries():
    return get_past_entries("gratitude")
