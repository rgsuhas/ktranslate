import unittest
from unittest.mock import MagicMock, patch
from core.language_router import LanguageRouter
from core.translation_engine import TranslationEngine

class TestLanguageRouter(unittest.TestCase):

    @patch('core.language_router.get_user_lang')
    def test_translation_routing(self, mock_get_user_lang):
        # Mock the user language preference
        mock_get_user_lang.return_value = "kn"
        
        # Create a mock translation engine
        mock_engine = MagicMock(spec=TranslationEngine)
        mock_engine.translate.return_value = "translated_text"

        # Initialize the language router with the mock engine
        router = LanguageRouter(engine=mock_engine)

        # Call the translate method with correct signature
        result = router.translate("This is English text", user_id=123)

        # Assert that the translate method of the mock engine was called
        # We don't assume the exact detected language, just that it was called with the right text and target
        mock_engine.translate.assert_called_once()
        call_args = mock_engine.translate.call_args
        self.assertEqual(call_args[0][0], "This is English text")  # First argument should be the text
        self.assertEqual(call_args[0][2], "kn")  # Third argument should be the target language

        # Assert that the result is the value returned by the mock engine
        self.assertEqual(result, "translated_text")

    @patch('core.language_router.get_user_lang')
    def test_translation_when_detected_lang_matches_target(self, mock_get_user_lang):
        # Mock the user language preference to match detected language
        mock_get_user_lang.return_value = "en"
        
        # Create a mock translation engine
        mock_engine = MagicMock(spec=TranslationEngine)
        mock_engine.translate.return_value = "translated_text"

        # Initialize the language router with the mock engine
        router = LanguageRouter(engine=mock_engine)

        # Call the translate method
        result = router.translate("This is English text", user_id=123)

        # When detected language matches user target, it should translate to Kannada
        mock_engine.translate.assert_called_once()
        call_args = mock_engine.translate.call_args
        self.assertEqual(call_args[0][0], "This is English text")
        self.assertEqual(call_args[0][1], "en")  # Source should be detected language
        self.assertEqual(call_args[0][2], "kn")  # Target should be Kannada (fallback)

        self.assertEqual(result, "translated_text")

if __name__ == '__main__':
    unittest.main()
