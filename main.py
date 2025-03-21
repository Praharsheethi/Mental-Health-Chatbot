from utils import create_chat_session, get_chat_response
import streamlit as st

st.title("Mental Health Chatbot")

user_input = st.text_input("You: ", key="user_input")
if user_input:
    response_text, sentiment = get_chat_response(chat_session, user_input)

    # Add to chat history
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("ai", response_text, sentiment))

    # Display messages
    with st.container():
        for entry in st.session_state.chat_history:
            if entry[0] == "user":
                emoji = "😊" if entry[2] == "positive" else "😢" if entry[2] == "negative" else "😐"
                st.markdown(f"<div class='chat-bubble user'>{entry[1]} {emoji}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble ai'>{entry[1]}</div>", unsafe_allow_html=True)
