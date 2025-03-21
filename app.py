import streamlit as st
from config import Config
import random
from utils import (
    apply_css, initialize_session, get_model_name,
    create_chat_session, get_chat_response
)
from sentiment import analyze_sentiment

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Mental Health Chatbot", layout="wide")

# Simple authentication function
def authenticate(username, password):
    # Replace with a database or more secure method in production
    return True

# Login Page
# Login Page (Now accepts any username & password)
def login():
    st.title("Login")
    username = st.text_input("Username")  
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username  # Store username in session
        st.success(f"Welcome, {username}!")
        st.rerun()  # Refresh page after login


# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# List of daily affirmations
affirmations = [
    "I am enough.",
    "I am resilient in the face of challenges.",
    "I choose myself.",
    "I am grateful for another day of life.",
    "I attract positivity and repel negativity."
    "Everything's gonna be okay!!"
]

# Function to display a random affirmation
def display_affirmation():
    affirmation = random.choice(affirmations)
    st.write(f"🌟 **Daily Affirmation:** {affirmation}")

# Main function
def main():
    initialize_session()

    # Login logic
    if not st.session_state['logged_in']:
        login()
        return  # Exit early if not logged in

    # Show affirmation after login
    display_affirmation()

    # Sidebar: Settings
    st.sidebar.title("Settings")
    st.session_state['dark_mode'] = st.sidebar.checkbox("Dark Mode", value=st.session_state['dark_mode'])

    model_choice = st.sidebar.selectbox(
        "Choose Model:",
        ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "Gemini 1.0 Pro"]
    )

    temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 1.0)
    top_p = st.sidebar.slider("Probability", 0.0, 1.0, 0.95)
    top_k = st.sidebar.slider("No. of Tokens", 0, 100, 64)
    max_output_tokens = st.sidebar.slider("Max Output Tokens", 1, 8192, 8192)

    apply_css(st.session_state['dark_mode'])

    st.title("🧠 Mental Health Chatbot")

    # 🛑 API Key (Kept as is)
    api_key = "AIzaSyDs1Q4r6swS1SNWiu_h7WzClq50f2Tmy3g"
    
    if api_key:
        model_name = get_model_name(model_choice)
        chat_session = create_chat_session(api_key, model_name, temperature, top_p, top_k, max_output_tokens)

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        # User Input for Chatbot
        user_input = st.text_input("You: ", key="user_input")
        if user_input.strip():  # Ensures empty messages are not sent
            response_text, sentiment = get_chat_response(chat_session, user_input)

            st.session_state.chat_history.append(("user", user_input, sentiment))
            st.session_state.chat_history.append(("ai", response_text, sentiment))

        # Chat History Display
        chat_container = st.container()
        with chat_container:
            for entry in st.session_state.chat_history:
                if entry[0] == "user":
                    emoji = "😊" if entry[2] == "positive" else "😢" if entry[2] == "negative" else "😐"
                    st.markdown(f"""
                        <div class="chat-message user">
                            <div class="chat-icon user"></div>
                            <div class="chat-bubble user">{entry[1]} {emoji}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="chat-message ai">
                            <div class="chat-icon ai"></div>
                            <div class="chat-bubble ai">{entry[1]} <br><small>Sentiment: {entry[2]}</small></div>
                        </div>
                    """, unsafe_allow_html=True)

    # 📌 Sidebar Features
    with st.sidebar.expander("🧘‍♀️ Breathing & Meditation Exercises"):
        st.write("Try these exercises to relax:")
        st.video("https://www.youtube.com/shorts/_fqr8XNubEI?feature=share")
        st.write("- **Deep Breathing**: Inhale for 4s, hold for 4s, exhale for 6s.")
        st.write("- **Box Breathing**: Inhale 4s, hold 4s, exhale 4s, hold 4s.")

    # 📖 Journaling (Sidebar)
    with st.sidebar.expander("📖 Journaling"):
        journal_entry = st.text_area("Write your thoughts:", key="journal_entry")
        if st.button("Save Entry"):
            if journal_entry.strip():  # Prevents saving empty entries
                if "journal_entries" not in st.session_state:
                    st.session_state["journal_entries"] = []
                st.session_state["journal_entries"].append(journal_entry)
                st.success("✅ Journal entry saved!")

    # Gratitude Journal (Sidebar)
    with st.sidebar.expander("🙏 Gratitude Journal"):
        gratitude_entry = st.text_area("What are you grateful for today?", key="gratitude_entry")
        if st.button("Save Gratitude"):
            if gratitude_entry.strip():  # Prevents saving empty entries
                if "gratitude_entries" not in st.session_state:
                    st.session_state["gratitude_entries"] = []
                st.session_state["gratitude_entries"].append(gratitude_entry)
                st.success("✅ Gratitude entry saved!")
                # Add Persona Selection to Sidebar
st.sidebar.title("AI Persona")
selected_persona = st.sidebar.selectbox(
    "Choose AI Personality",
    ["Supportive Friend", "Coach", "Therapist-like"]
)
st.session_state["selected_persona"] = selected_persona  # Store selection

st.write(f"🌟 You are chatting with a {selected_persona} persona.")
# Display Alert for Emotional Support
if st.session_state.get("show_alert", False):
    st.error("⚠️ It seems like you're going through a tough time. You're not alone. Would you like to try journaling or talk to someone?")
    
    # Add support options
    if st.button("📖 Start Journaling"):
        st.session_state["writing_journal"] = True

    if st.button("🧘 Breathing Exercise"):
        st.write("Take a deep breath... Inhale for 4 seconds, hold for 7, and exhale for 8. Try it a few times! 💙")

    if st.button("📞 Need Professional Help?"):
        st.markdown("[Click here for mental health resources](https://www.mentalhealth.gov/)")  # Replace with real helpline


# Run the app
if __name__ == "__main__":
    main()
