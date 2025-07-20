import unittest
from unittest.mock import MagicMock
from core.language_router import LanguageRouter
from core.translation_engine import TranslationEngine

class TestLanguageRouter(unittest.TestCase):

    def test_translation_routing(self):
        # Create a mock translation engine
        mock_engine = MagicMock(spec=TranslationEngine)
        mock_engine.translate.return_value = "translated_text"

        # Initialize the language router with the mock engine
        router = LanguageRouter(engine=mock_engine)

        # Call the translate method
        result = router.translate("test text", tgt_lang="kn")

        # Assert that the translate method of the mock engine was called with the correct arguments
        # langdetect will detect 'en' for "test text"
        mock_engine.translate.assert_called_once_with("test text", "en", "kn")

        # Assert that the result is the value returned by the mock engine
        self.assertEqual(result, "translated_text")

if __name__ == '__main__':
    unittest.main()
