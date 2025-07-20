# bot/session_state.py

user_lang_pref = {}

def set_user_lang(user_id: int, lang: str):
    """Sets the preferred target language for a given user."""
    user_lang_pref[user_id] = lang

def get_user_lang(user_id: int) -> str:
    """Gets the preferred target language for a given user, defaulting to 'kn' (Kannada)."""
    return user_lang_pref.get(user_id, "kn")  # Default to Kannada
