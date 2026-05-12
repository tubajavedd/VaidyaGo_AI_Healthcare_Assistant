import os
import whisper
import tempfile
import logging

try:
    from groq import Groq
except ImportError:
    Groq = None

logger = logging.getLogger(__name__)

class VoiceService:
    _model = None

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            logger.info("Loading Whisper model (base)...")
            cls._model = whisper.load_model("base")
        return cls._model

    @staticmethod
    def transcribe(audio_file):
        """
        Transcribes an audio file using Groq Whisper or local OpenAI Whisper.
        """
        try:
            # Create a temporary file to save the uploaded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Try Groq API first
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key and Groq:
                try:
                    logger.info("Using Groq Whisper for transcription...")
                    client = Groq(api_key=api_key)
                    with open(tmp_path, "rb") as file:
                        transcription = client.audio.transcriptions.create(
                            file=(tmp_path, file.read()),
                            model="whisper-large-v3",
                            response_format="text"
                        )
                    os.remove(tmp_path)
                    return transcription.strip()
                except Exception as groq_e:
                    logger.warning(f"Groq transcription failed, falling back to local: {str(groq_e)}")

            # Fallback to local Whisper
            logger.info("Using local Whisper for transcription...")
            model = VoiceService._get_model()
            result = model.transcribe(tmp_path)
            
            # Clean up temp file
            os.remove(tmp_path)
            
            return result.get("text", "").strip()
        except Exception as e:
            logger.error(f"Whisper transcription error: {str(e)}")
            return None
