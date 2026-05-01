from langdetect import detect


class LanguageService:

    @staticmethod
    def detect_language(text: str) -> str:
        try:
            return detect(text)
        except Exception:
            return "en"
