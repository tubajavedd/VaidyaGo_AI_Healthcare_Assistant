import os
import whisper
import tempfile
import logging

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
        Transcribes an audio file using OpenAI Whisper.
        """
        try:
            # Create a temporary file to save the uploaded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            model = VoiceService._get_model()
            result = model.transcribe(tmp_path)
            
            # Clean up temp file
            os.remove(tmp_path)
            
            return result.get("text", "").strip()
        except Exception as e:
            logger.error(f"Whisper transcription error: {str(e)}")
            return None
