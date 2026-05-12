try:
    from TTS.api import TTS
    print("TTS is installed")
    # Just checking if we can instantiate it without downloading a huge model immediately
    # or list available models
    tts = TTS()
    print("Available models (first 5):", tts.list_models()[:5])
except ImportError:
    print("TTS is NOT installed")
except Exception as e:
    print(f"Error: {e}")
