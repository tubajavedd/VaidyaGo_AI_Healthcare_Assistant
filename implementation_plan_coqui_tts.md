# Integrate Coqui TTS into TTSService

The user wants to setup Coqui TTS for the project. The current implementation uses `edge_tts`. I will update `TTSService` to use Coqui TTS as the primary engine, with a fallback to `edge_tts` to ensure reliability.

## User Review Required

> [!IMPORTANT]
> Coqui TTS requires significant system resources (CPU/GPU) and may take some time to initialize for the first request. I will implement it as a singleton to minimize initialization overhead.
> Also, Coqui TTS will attempt to download the required models on the first run if they are not present. This might require an internet connection and some time.
> Please ensure that the `TTS` package is installed in the Python environment used by the Django server.

## Proposed Changes

### [Backend]

#### [MODIFY] [tts_service.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot/services/tts_service.py)
- Import `TTS` from `TTS.api`.
- Initialize a `TTS` instance as a class-level or singleton object.
- Update `generate_speech` method to use Coqui TTS.
- Maintain the existing `edge_tts` logic as a fallback.
- Handle Hindi and English language detection for model/speaker selection.

## Verification Plan

### Automated Tests
- I will create a test script `vaidyaGo/vaidyaGo/scratch/verify_coqui_integration.py` to call `TTSService.generate_speech` and check if an audio file is generated in the `media/tts` folder.

### Manual Verification
- The user can test the chatbot in the frontend and check if the audio response is played using the new Coqui TTS engine.
