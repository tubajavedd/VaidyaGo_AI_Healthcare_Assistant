# Walkthrough - Only Female Voices for TTS

I have updated the `TTSService` to strictly use female voices across all supported text-to-speech engines and updated the voice sample directory for Coqui TTS.

## Changes Made

### [Backend]

#### [tts_service.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot/services/tts_service.py)

- **Google Cloud TTS**: Restricted to `FEMALE` gender. For English, switched from `en-IN-Neural2-B` (Male) to `en-IN-Neural2-A` (Female).
- **edge-tts**: Switched English voice from `en-IN-PrabhatNeural` (Male) to `en-IN-NeerjaNeural` (Female).
- **pyttsx3**: Updated fallback logic to prioritize female voices (`female`, `zira`, `kalpana`) for all languages.
- **Coqui TTS**: Updated the voice sample directory to `media/tts/voicess` and the target file to `female_voice.wav`.

### [Media]

- **Directory Created**: Created `media/tts/voicess` to store the female voice sample for Coqui TTS.

## How to Test

1. **Coqui TTS**: Place a female voice sample named `female_voice.wav` in the `media/tts/voicess` directory.
2. **General TTS**: Interact with the chatbot in English or Hindi/Hinglish. The response audio should now use a female voice.
3. **Fallbacks**: If Google Cloud TTS is unavailable, the system will fall back to edge-tts (Female) and then pyttsx3 (Female), ensuring a consistent experience.

> [!NOTE]
> No changes were made to the frontend or other backend components as requested.
