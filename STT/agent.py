import os
import asyncio
import json
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)
import aiohttp
from tools.session_tools import SessionTools

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
NLU_SERVICE_URL = os.getenv("NLU_SERVICE_URL", "http://127.0.0.1:8000")

class STTAgent:
    def __init__(self, db_url: str):
        if not DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is not set in environment.")
            
        self.dg_client = DeepgramClient(DEEPGRAM_API_KEY)
        self.session_tools = SessionTools(db_url)
        self.last_final_transcript = ""
        self.session_id = None
        self.loop = None
        self.ws_session = None
        self.ws_connection = None
        self.listener_task = None

    async def _listen_to_nlu(self):
        """Background task to continuously receive messages from NLU WebSocket."""
        try:
            async for msg in self.ws_connection:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    print(f"NLU Intent: {data.get('intent')} (Confidence: {data.get('intent_confidence')})")
                    print(f"NLU Answer: {data.get('answer_text')}")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        except Exception as e:
            print(f"NLU listener error: {e}")

    async def run(self, session_id: str, audio_generator, language_code: str):
        self.session_id = session_id
        self.loop = asyncio.get_running_loop()
        dg_connection = None
        
        # Connect to NLU via WebSockets using aiohttp with keepalive heartbeats
        try:
            ws_url = NLU_SERVICE_URL.replace("http://", "ws://").replace("https://", "wss://") + "/ws"
            self.ws_session = aiohttp.ClientSession()
            # heartbeat=30 ensures the client sends a PING to the server every 30 seconds
            # so the operating system/proxy never closes the idle connection.
            self.ws_connection = await self.ws_session.ws_connect(ws_url, heartbeat=30.0)
            self.listener_task = self.loop.create_task(self._listen_to_nlu())
            print("[INFO] Connected to NLU WebSocket!")
        except Exception as e:
            print(f"[WARN] Failed to connect to NLU WebSocket: {e}")

        try:
            dg_connection = self.dg_client.listen.live.v("1")
            
            dg_connection.on(LiveTranscriptionEvents.Transcript, self.handle_transcript)
            dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, self.handle_utterance_end)
            dg_connection.on(LiveTranscriptionEvents.Error, self.handle_error)
            
            options = LiveOptions(
                model="nova-3", 
                language=language_code,
                smart_format=True,
                endpointing=300,   
                utterance_end_ms="1200",
                interim_results=True,
                encoding="linear16",
                sample_rate=16000,
                channels=1
            )
            
            if not dg_connection.start(options):
                return
            
            print("Start Speaking")

            async for data in audio_generator:
                dg_connection.send(data)

        except Exception as e:
            pass
        finally:
            # Cleanup
            if dg_connection:
                dg_connection.finish()
            if self.listener_task:
                self.listener_task.cancel()
            if self.ws_connection and not self.ws_connection.closed:
                await self.ws_connection.close()
            if self.ws_session and not self.ws_session.closed:
                await self.ws_session.close()

    def handle_transcript(self, connection, result, **kwargs):
        if not result or not self.session_id:
            return
            
        sentence = ""

        try:
            if hasattr(result, "channel") and result.channel.alternatives:
                alt = result.channel.alternatives[0]
                sentence = alt.transcript or ""

                is_final = getattr(result, 'is_final', False)
                speech_final = getattr(result, 'speech_final', False)
                
                if sentence.strip():
                    if not is_final and not speech_final:
                        pass
                        
                    if is_final:
                        # Append the chunk to our ongoing complete utterance buffer
                        if self.last_final_transcript:
                             self.last_final_transcript += f" {sentence}"
                        else:
                             self.last_final_transcript = sentence

                        print(f"Transcript : {sentence}")
                    
                # If speech_final is true, Deepgram detected a pause. 
                # This is our primary trigger to complete the utterance!
                if speech_final and self.last_final_transcript:
                    completed_utterance = self.last_final_transcript
                    print(f"Final Transcript : {completed_utterance}")

                    if self.loop and not self.loop.is_closed():
                        async def save_to_db_and_nlu(sid, txt):
                            # 1. IMMEDIATE: Stream to NLU via WebSocket FIRST so LLM starts generating
                            if self.ws_connection and not self.ws_connection.closed:
                                payload = {
                                    "session_id": sid,
                                    "user_id": "caller",
                                    "utterance": txt,
                                    "detected_language": "en"
                                }
                                try:
                                    await self.ws_connection.send_json(payload)
                                except Exception as nlu_err:
                                    print(f"Failed to stream to NLU WebSocket: {nlu_err}")
                                    
                            # 2. BACKGROUND: Save transcript to Neon DB (takes a few hundred ms)
                            await asyncio.to_thread(self.session_tools.update_transcript, sid, txt, "en")

                        asyncio.run_coroutine_threadsafe(
                            save_to_db_and_nlu(self.session_id, completed_utterance), 
                            self.loop
                        )

                    self.last_final_transcript = ""

        except Exception as e:
            pass

    def handle_utterance_end(self, connection, utterance_end, **kwargs):
        if not self.session_id:
            return

        # UtteranceEnd acts as a fallback for noisy environments where
        # endpointing/speech_final might fail to detect a pause.
        if self.last_final_transcript:
            completed_utterance = self.last_final_transcript
            print(f"Final Transcript (Fallback) : {completed_utterance}")

            if self.loop and not self.loop.is_closed():
                async def save_to_db_and_nlu(sid, txt):
                    # 1. IMMEDIATE: Stream to NLU via WebSocket FIRST 
                    if self.ws_connection and not self.ws_connection.closed:
                        payload = {
                            "session_id": sid,
                            "user_id": "caller",
                            "utterance": txt,
                            "detected_language": "en"
                        }
                        try:
                            await self.ws_connection.send_json(payload)
                        except Exception as nlu_err:
                            print(f"Failed to stream to NLU WebSocket: {nlu_err}")
                            
                    # 2. BACKGROUND: Save transcript to DB
                    await asyncio.to_thread(self.session_tools.update_transcript, sid, txt, "en")

                asyncio.run_coroutine_threadsafe(
                    save_to_db_and_nlu(self.session_id, completed_utterance), 
                    self.loop
                )

            self.last_final_transcript = ""

    def handle_error(self, connection, error, **kwargs):
        pass