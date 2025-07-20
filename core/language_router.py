from langdetect import detect
from core.translation_engine import TranslationEngine
from services import google_translate # Keep for now, will be replaced by engine instance
from bot.session_state import get_user_lang # Import get_user_lang

class LanguageRouter:
    def __init__(self, engine: TranslationEngine):
        self.engine = engine

    def translate(self, text: str, user_id: int) -> str:
        detected_lang = detect(text)
        user_target = get_user_lang(user_id)

        # Determine actual source and target languages for the translation engine
        if detected_lang == user_target:
            # If user writes in their preferred target language, invert the translation
            # For now, fallback to Kannada if the user's target is the detected language
            # A more robust solution might allow user to specify a secondary fallback or cycle through languages
            src, tgt = user_target, "kn"  # Translate from user's target to Kannada
        else:
            src, tgt = detected_lang, user_target

        # Call the underlying translation engine
        return self.engine.translate(text, src, tgt)

# Example usage (for testing/demonstration, not used in main bot flow):
if __name__ == '__main__':
    # This is a simple example. In a real application, the engine would be chosen dynamically.
    # For this example, we'll use a mock engine or a direct instance if possible.
    class MockTranslationEngine(TranslationEngine):
        def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
            return f"Mock Translated from {src_lang} to {tgt_lang}: {text}"

    mock_engine = MockTranslationEngine()
    router = LanguageRouter(engine=mock_engine)

    # Simulate user 1 setting preference to English
    from bot.session_state import set_user_lang
    set_user_lang(1, "en")

    # Test case 1: User writes in English, target is English -> should invert to Kannada
    translated_text_1 = router.translate("Hello, how are you?", user_id=1)
    print(f"Test 1 (English input, English target): {translated_text_1}")

    # Test case 2: User writes in Kannada, target is English
    translated_text_2 = router.translate("ನೀವು ಹೇಗಿದ್ದೀರಿ?", user_id=1)
    print(f"Test 2 (Kannada input, English target): {translated_text_2}")

    # Simulate user 2 with default Kannada target
    translated_text_3 = router.translate("Hello, world!", user_id=2)
    print(f"Test 3 (English input, default Kannada target): {translated_text_3}")