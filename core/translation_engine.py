class TranslationEngine:
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        raise NotImplementedError("Implement in subclass")
