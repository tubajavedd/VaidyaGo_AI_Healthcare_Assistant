import os
import uuid
import logging
from django.conf import settings
import subprocess
import threading
import shutil

logger = logging.getLogger(__name__)

# Pronunciation corrections
corrections = {
    "VaidyaGo":    "Vaid-ya-Go",
    "appointment": "uh-point-ment",
    "prescription":"pre-scrip-shun",
    "Namaste":     "Nuh-muh-stay",
}

def fix_pronunciation(text):
    for word, phonetic in corrections.items():
        text = text.replace(word, phonetic)
    return text

def add_natural_pauses(text, use_ssml=False):
    if use_ssml:
        # SSML specific breaks
        text = text.replace(",", ', <break time="300ms"/>')
        text = text.replace("।", '. <break time="500ms"/>')
        text = text.replace("!", '! <break time="400ms"/>')
        text = text.replace("?", '? <break time="400ms"/>')
        return f"<speak>{text}</speak>"
    else:
        text = text.replace(",", ", ... ")
        text = text.replace("।", ". ")
        text = text.replace("!", "! ... ")
        text = text.replace("?", "? ... ")
        return text

class CoquiTTS:
    _instance = None
    _lock = threading.Lock()
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    try:
                        from TTS.api import TTS
                        # Using XTTS v2 for best cloning and multilingual support
                        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
                        logger.info(f"Loading Coqui TTS model: {model_name}...")
                        cls._model = TTS(model_name).to("cpu") # Use .to("cuda") if GPU is available
                        cls._instance = cls()
                    except Exception as e:
                        logger.error(f"Failed to load Coqui TTS: {str(e)}")
                        return None
        return cls._instance

    def generate(self, text, output_path, speaker_wav=None, language="en"):
        try:
            if not self._model:
                return False
            
            # Default speaker if no wav provided
            # In xtts_v2, speaker_wav is mandatory for cloning or use a preset
            if not speaker_wav:
                # Use a default voice if cloning is not possible
                self._model.tts_to_file(text=text, file_path=output_path, speaker="Ana Paula89", language=language)
            else:
                self._model.tts_to_file(text=text, file_path=output_path, speaker_wav=speaker_wav, language=language)
            return True
        except Exception as e:
            logger.error(f"Coqui generation error: {str(e)}")
            return False

class TTSService:
    @staticmethod
    def generate_speech(text):
        """
        Generates an audio file from text using Google Cloud TTS (Primary), edge-tts, gTTS, or offline pyttsx3 fallback.
        """
        if not text or not text.strip():
            return None

        # Detect language / script
        is_devanagari = any('\u0900' <= c <= '\u097f' for c in text)
        hinglish_words = {'hai', 'hoon', 'aap', 'kaise', 'haan', 'nahi', 'ko', 'se', 'mein', 'aur', 'ji', 'namaste', 'bataiye', 'kya', 'karo', 'raha', 'rahi', 'hu', 'sab', 'kuch', 'hoga', 'chahiye'}
        words_in_text = set(text.lower().replace('.', ' ').replace(',', ' ').replace('?', ' ').replace('!', ' ').split())
        is_hinglish = bool(words_in_text.intersection(hinglish_words))
        is_hindi = is_devanagari or is_hinglish

        lang = 'hi-IN' if is_devanagari else 'en-IN'

        # Apply pronunciation fixes
        processed_text_base = fix_pronunciation(text)

        # Create tts directory
        tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts')
        if not os.path.exists(tts_dir):
            os.makedirs(tts_dir, exist_ok=True)

        filename = f"vado_voice_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(tts_dir, filename)

        # 0. Try Coqui TTS (User Voice Cloning)
        try:
            coqui = CoquiTTS.get_instance()
            if coqui:
                # Target the specific filename requested by the user
                reference_wav = os.path.join(settings.MEDIA_ROOT, 'tts', 'myvoice.wav.m4a')
                if not os.path.exists(reference_wav):
                    reference_wav = os.path.join(settings.MEDIA_ROOT, 'voice_clones', 'myvoice.wav.m4a')
                
                if os.path.exists(reference_wav):
                    coqui_lang = 'hi' if is_hindi else 'en'
                    logger.info(f"Using XTTS v2 Cloning | Lang: {coqui_lang} | Ref: {reference_wav}")
                    
                    # Exactly as requested: tts.tts_to_file(text=..., speaker_wav=..., language=..., file_path=...)
                    if coqui.generate(processed_text_base, filepath, speaker_wav=reference_wav, language=coqui_lang):
                        return f"{settings.MEDIA_URL}tts/{filename}"
        except Exception as coqui_err:
            logger.warning(f"XTTS v2 failed: {str(coqui_err)}")

        # 1. Try Google Cloud TTS (Neural)
        try:
            from google.cloud import texttospeech
            
            ssml_text = add_natural_pauses(processed_text_base, use_ssml=True)
            
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

            # Voice Quality
            # Use Female for both Hindi and English
            selected_voice_name = "hi-IN-Neural2-A" if is_hindi else "en-IN-Neural2-A"
            selected_gender = texttospeech.SsmlVoiceGender.FEMALE

            voice = texttospeech.VoiceSelectionParams(
                language_code=lang,
                name=selected_voice_name,
                ssml_gender=selected_gender
            )

            # Talking Style: speaking_rate 0.9, pitch +2.0
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.9,
                pitch=2.0
            )

            logger.info("Attempting Google Cloud TTS (hi-IN-Neural2-A)...")
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            with open(filepath, "wb") as out:
                out.write(response.audio_content)
                
            return f"{settings.MEDIA_URL}tts/{filename}"

        except Exception as gc_error:
            logger.warning(f"Google Cloud TTS failed (missing credentials?), trying edge-tts: {str(gc_error)}")
            
            # 2. Fallback to edge-tts
            try:
                # Female for both Hindi and English
                if is_hindi:
                    voice_name = "hi-IN-SwaraNeural" # Swara handles both Devanagari and Hinglish perfectly
                else:
                    voice_name = "en-IN-NeerjaNeural" # Female Indian English

                logger.info(f"Generating speech using edge-tts voice: {voice_name}")
                
                # subprocess run to avoid asyncio event loop conflicts
                subprocess.run([
                    'edge-tts', 
                    '--voice', voice_name, 
                    '--text', processed_text_base, 
                    '--rate=-10%',
                    '--write-media', filepath
                ], check=True)
                
                return f"{settings.MEDIA_URL}tts/{filename}"
                
            except Exception as edge_error:
                logger.warning(f"edge-tts failed, falling back to gTTS: {str(edge_error)}")
            
                # 3. Fallback to gTTS / pyttsx3
                processed_text = add_natural_pauses(processed_text_base, use_ssml=False)
                lang_gtts = 'hi' if is_hindi else 'en'
                
                try:
                    from gtts import gTTS
                    logger.info(f"Generating speech using gTTS in language: {lang_gtts}")
                    if lang_gtts == 'en':
                        tts = gTTS(text=processed_text, lang=lang_gtts, tld='co.in', slow=False)
                    else:
                        tts = gTTS(text=processed_text, lang=lang_gtts, slow=False)
                        
                    tts.save(filepath)
                    return f"{settings.MEDIA_URL}tts/{filename}"
                    
                except Exception as e:
                    logger.warning(f"gTTS failed, falling back to offline pyttsx3: {str(e)}")
                    try:
                        import pyttsx3
                        engine = pyttsx3.init()
                        
                        engine.setProperty('rate', 160)
                        engine.setProperty('volume', 0.9)
                        try:
                            engine.setProperty('pitch', 1.2)
                        except Exception:
                            pass

                        voices = engine.getProperty('voices')
                        for voice in voices:
                            # Prioritize female voices for all languages
                            if 'female' in voice.name.lower() or 'zira' in voice.name.lower() or 'kalpana' in voice.name.lower():
                                engine.setProperty('voice', voice.id)
                                break

                        filepath_wav = filepath.replace('.mp3', '.wav')
                        filename_wav = filename.replace('.mp3', '.wav')
                        
                        logger.info("Saving audio via pyttsx3 offline...")
                        engine.save_to_file(processed_text, filepath_wav)
                        engine.runAndWait()
                        return f"{settings.MEDIA_URL}tts/{filename_wav}"
                    except ImportError as ie:
                        logger.error(f"Missing required TTS package. Error: {str(ie)}")
                        return None
                    except Exception as pyttsx3_e:
                        logger.error(f"TTS generation error: {str(pyttsx3_e)}")
                        return None
