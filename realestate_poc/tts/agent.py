import os
import io
import wave
import pyaudio
import asyncio
from typing import Iterator
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
if ELEVEN_API_KEY:
    client = ElevenLabs(api_key=ELEVEN_API_KEY)
else:
    client = None
    print("[WARN] ELEVEN_API_KEY not found in .env")

# ElevenLabs PCM configuration
SAMPLE_RATE = 16000
CHANNELS = 1

def generate_and_play_voice_sync(text: str):
    """
    Synchronously generates TTS audio from ElevenLabs as raw PCM bytes
    and plays it directly to the PC speaker using PyAudio.
    """
    if not client:
        print("[WARN] ElevenLabs client not initialized. Cannot speak.")
        return
        
    try:
        # Request raw PCM audio instead of compressed MP3 for immediate streaming
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id="pNInz6obpgDQGcFmaJgB", # Using the same voice from voice-agent-simple
            model_id="eleven_turbo_v2",
            output_format="pcm_16000"
        )
        
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        output=True)
                        
        print(f"[TTS] Speaking: '{text}'")
        
        # Stream the bytes directly to the speaker as they arrive from the API
        for chunk in audio_stream:
            if chunk:
                stream.write(chunk)
                
        # Clean up audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    except Exception as e:
        print(f"[ERROR] Failed to play TTS audio: {e}")

async def generate_and_play_voice(text: str):
    """
    Asynchronous wrapper to run the synchronous audio streaming 
    in a separate thread so it doesn't block the asyncio event loop.
    """
    await asyncio.to_thread(generate_and_play_voice_sync, text)
