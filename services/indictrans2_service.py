from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from core.translation_engine import TranslationEngine

class IndicTransService(TranslationEngine):
    def __init__(self, model_name="ai4bharat/indictrans2-en-indic"):
        """
        Initializes the IndicTrans2 service with a pre-trained model.
        For other language pairs, you may need to load a different model.
        e.g. "ai4bharat/indictrans2-indic-en-dist-200M"
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Translates text using the IndicTrans2 model.

        Note: The model expects a special token format for the target language.
        Example: "<2kn> This is a test." for English to Kannada.
        We will need to map standard ISO 639-1 language codes to these tokens.
        """
        # This is a simplified example. A robust implementation would need a mapping
        # from standard language codes (e.g., 'en', 'kn') to the model's specific tokens.
        # For now, we'll assume a simple case.
        
        # Example for English to Kannada
        if src_lang == 'en' and tgt_lang == 'kn':
            input_text = f"<2kn> {text}"
        else:
            # This is where a more sophisticated mapping would be needed.
            # For now, we'll just return an error message.
            return f"Translation from {src_lang} to {tgt_lang} is not supported by this model."

        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=128)
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
