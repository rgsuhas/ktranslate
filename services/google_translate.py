from deep_translator import GoogleTranslator
from core.translation_engine import TranslationEngine

class GoogleTranslateService(TranslationEngine):
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Translates text using the deep-translator library.
        """
        return GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
