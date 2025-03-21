# personas.py

PERSONALITY_PROFILES = {
    "Supportive Friend": {
        "tone": "warm and friendly",
        "style": "casual and reassuring",
        "example_response": "I'm here for you! It's okay to feel this way. How can I support you today?",
    },
    "Coach": {
        "tone": "motivational and solution-focused",
        "style": "direct and goal-oriented",
        "example_response": "Let's break this down! What’s one small step you can take right now?",
    },
    "Therapist-like": {
        "tone": "calm and reflective",
        "style": "thoughtful and open-ended",
        "example_response": "That sounds really tough. What do you think might help you cope with this feeling?",
    },
}

def get_personality_response(personality, user_input):
    """
    Modify chatbot responses based on the selected personality.
    """
    profile = PERSONALITY_PROFILES.get(personality, PERSONALITY_PROFILES["Supportive Friend"])
    
    if "stressed" in user_input.lower():
        return f"{profile['example_response']} Take a deep breath, and let's talk about it. 💙"

    return f"{profile['example_response']} How are you feeling about this?"
