import os
import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

from audio.mic_stream import get_mic_stream
from workflow import realestate_workflow
from tools.session_tools import SessionTools

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Initial dummy session state for local testing (same as original Agent 1)
DUMMY_SESSION_ID = "test_local_mic_003"
DUMMY_SESSION_STATE = {
    "session_id": DUMMY_SESSION_ID,
    "user_id": "debug_user",
    "created_at": datetime.now(timezone.utc).isoformat() + "Z",
    "updated_at": datetime.now(timezone.utc).isoformat() + "Z",
    "state": {
        "caller_number": "local_mic",
        "caller_name": "Dev User",
        "language": "en",
        "call_start_time": datetime.now(timezone.utc).isoformat() + "Z",
        "conversation": [],
        "entities": {},
        "intent_history": [],
        "lead_scoring": {},
        "sentiment": {},
        "call_summary": "",
        "next_actions": []
    },
    "metadata": {
        "workflow_version": "2.0",
        "language_detected_by": "default_english",
        "stt_engine": "deepgram-nova-3-streaming"
    }
}

class RealEstatePipeline:
    def __init__(self):
        if not DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY is not set.")
        self.dg_client = DeepgramClient(DEEPGRAM_API_KEY)
        self.session_id = "test_local_mic_003"
        self.last_final_transcript = ""
        self.loop = None

    async def trigger_workflow(self, utterance: str):
        print(f"\n>> Sending to Agno Workflow: '{utterance}'")
        
        # Trigger the in-process synchronous agility of Agno Workflows
        try:
            # We pass a dict because our prepare_context_step expects utterance_data
            input_data = {
                "utterance": utterance,
                "session_id": self.session_id
            }
            # Agno Workflow arun returns a RunResponse asynchronously.
            response = await realestate_workflow.arun(input_data)
            final_output = getattr(response, "content", None)

            if final_output:
                if isinstance(final_output, dict) and "error" in final_output:
                    print(f"Workflow Error: {final_output['error']}")
                elif isinstance(final_output, dict):
                    print(f"\n[WF NLU Intent]: {final_output.get('intent')} (Conf: {final_output.get('confidence')})")
                    print(f"[WF NLU Action]: {final_output.get('action')}")
                    print(f"[WF NLU Answer]: {final_output.get('answer')}")
                else:
                    print(f"\n[WF Raw Output]: {final_output}")
            
        except Exception as e:
            print(f"[WARN] Agno Workflow failed: {e}")

    def handle_transcript(self, connection, result, **kwargs):
        if not result: return
        sentence = ""
        try:
            if hasattr(result, "channel") and result.channel.alternatives:
                alt = result.channel.alternatives[0]
                sentence = alt.transcript or ""
                
                is_final = getattr(result, 'is_final', False)
                speech_final = getattr(result, 'speech_final', False)
                
                if sentence.strip():
                    if is_final:
                        if self.last_final_transcript:
                             self.last_final_transcript += f" {sentence}"
                        else:
                             self.last_final_transcript = sentence
                        print(f"Transcript : {sentence}")
                    
                if speech_final and self.last_final_transcript:
                    completed_utterance = self.last_final_transcript
                    # Run workflow asynchronously without blocking Deepgram audio
                    if self.loop and not self.loop.is_closed():
                        self.loop.create_task(self.trigger_workflow(completed_utterance))
                    self.last_final_transcript = ""
        except Exception as e:
            pass

    def handle_utterance_end(self, connection, utterance_end, **kwargs):
        if self.last_final_transcript:
            completed_utterance = self.last_final_transcript
            if self.loop and not self.loop.is_closed():
                self.loop.create_task(self.trigger_workflow(completed_utterance))
            self.last_final_transcript = ""

    async def start(self):
        self.loop = asyncio.get_running_loop()
        dg_connection = None

        # Create the session row in DB (same as original Agent 1)
        if DATABASE_URL:
            session_tools = SessionTools(DATABASE_URL)
            await asyncio.to_thread(session_tools.create_dummy_session, DUMMY_SESSION_ID, DUMMY_SESSION_STATE)
            print(f"Session '{DUMMY_SESSION_ID}' ready in DB.")

        try:
            dg_connection = self.dg_client.listen.websocket.v("1")
            dg_connection.on(LiveTranscriptionEvents.Transcript, self.handle_transcript)
            dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, self.handle_utterance_end)
            
            options = LiveOptions(
                model="nova-3", 
                language="en",
                smart_format=True,
                endpointing=300,   
                utterance_end_ms="1200",
                interim_results=True,
                encoding="linear16",
                sample_rate=16000,
                channels=1
            )
            
            if not dg_connection.start(options):
                print("Failed to start Deepgram")
                return

            print("\n============ REAL ESTATE POC ============")
            print("Agno Workflow Integrated. Ready for Audio.")
            print("Start Speaking...")

            audio_generator = get_mic_stream()
            async for data in audio_generator:
                dg_connection.send(data)

        except KeyboardInterrupt:
            pass
        finally:
            if dg_connection:
                dg_connection.finish()

if __name__ == "__main__":
    pipeline = RealEstatePipeline()
    asyncio.run(pipeline.start())
