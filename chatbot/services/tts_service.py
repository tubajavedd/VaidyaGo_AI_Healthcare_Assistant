import os
import uuid
import logging
from gtts import gTTS
from django.conf import settings

logger = logging.getLogger(__name__)

class TTSService:
    @staticmethod
    def generate_speech(text):
        """
        Generates an MP3 from text using gTTS and returns the URL.
        Automatically detects Hindi characters to choose the correct voice.
        """
        try:
            # Create tts directory in media if it doesn't exist
            tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
            if not os.path.exists(tts_dir):
                os.makedirs(tts_dir, exist_ok=True)

            # Detect language for gTTS (simple detection)
            # If text has Hindi characters (\u0900 to \u097F), use 'hi'
            gtts_lang = 'hi' if any('\u0900' <= c <= '\u097f' for c in text) else 'en'
            
            # Generate unique filename
            filename = f"vado_voice_{uuid.uuid4().hex[:8]}.mp3"
            filepath = os.path.join(tts_dir, filename)

            # Create gTTS object and save to file
            # lang='en' uses a natural sounding English, 'hi' for Hindi
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
            tts.save(filepath)

            # Return the relative URL (e.g., /media/tts/filename.mp3)
            return f"{settings.MEDIA_URL}tts/{filename}"
        except Exception as e:
            logger.error(f"TTS generation error: {str(e)}")
            return None
