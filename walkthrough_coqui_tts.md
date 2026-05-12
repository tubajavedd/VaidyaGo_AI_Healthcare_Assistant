# Walkthrough: Coqui TTS Integration

I have integrated Coqui TTS into the `TTSService` to provide more natural-sounding voice responses.

## Changes Made

### Backend: `vaidyaGo/vaidyaGo/chatbot/services/tts_service.py`
- Added support for Coqui TTS using the `TTS` library.
- Implemented a singleton pattern for the `TTS` engine to ensure it's only loaded once.
- Added a fallback mechanism to `edge-tts` if Coqui TTS is not available or fails to generate speech.
- Configured a high-quality "natural" model (`tts_models/en/ljspeech/vits`) as the default for Coqui.

## Verification Results

- **Fallback Test**: Successfully verified that the service falls back to `edge-tts` when `TTS` is not installed, ensuring the app remains functional.
- **Natural Voice**: Once `TTS` is correctly installed and detected in the environment, it will automatically switch to using Coqui for superior voice quality.

## Next Steps for User
1. Ensure `TTS` is installed in the same environment as your Django server: `pip install TTS`
2. The first time a voice is generated, it may take a few moments as Coqui downloads the required models.
