#!/usr/bin/env python3
"""
Test Transcribe Streaming STT locally.
Generates a short test audio and transcribes it using the streaming API.
"""
import sys
import os
import time
import asyncio
import struct
import base64

# Add the app_message directory to path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src_aws', 'app_message'))

REGION = 'us-east-1'
SAMPLE_RATE = 16000


def generate_silence_wav(duration_s=2.0) -> bytes:
    """Generate a silent WAV file for testing connectivity."""
    num_samples = int(SAMPLE_RATE * duration_s)
    # WAV header
    data_size = num_samples * 2  # 16-bit = 2 bytes per sample
    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + data_size, b'WAVE',
        b'fmt ', 16, 1, 1, SAMPLE_RATE, SAMPLE_RATE * 2, 2, 16,
        b'data', data_size)
    # Silent PCM data
    pcm = b'\x00\x00' * num_samples
    return header + pcm


async def test_streaming():
    """Test the Transcribe Streaming API directly."""
    from amazon_transcribe.client import TranscribeStreamingClient
    from amazon_transcribe.handlers import TranscriptResultStreamHandler
    from amazon_transcribe.model import TranscriptEvent

    transcript_parts = []

    class TestHandler(TranscriptResultStreamHandler):
        async def handle_transcript_event(self, transcript_event: TranscriptEvent):
            results = transcript_event.transcript.results
            for result in results:
                if not result.is_partial:
                    for alt in result.alternatives:
                        transcript_parts.append(alt.transcript)
                        print(f"  📝 Final: '{alt.transcript}'")
                else:
                    for alt in result.alternatives:
                        print(f"  ⏳ Partial: '{alt.transcript}'")

    print("🔌 Creating TranscribeStreamingClient...")
    client = TranscribeStreamingClient(region=REGION)

    print("🚀 Starting stream transcription...")
    start = time.time()
    
    stream = await client.start_stream_transcription(
        language_code="es-US",
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm",
    )
    
    connect_time = time.time() - start
    print(f"✅ Stream connected in {connect_time:.2f}s")

    handler = TestHandler(stream.output_stream)

    # Send silence (just to test connectivity)
    async def send_audio():
        print("📤 Sending 2s of silence...")
        silence = b'\x00\x00' * SAMPLE_RATE * 2  # 2 seconds
        chunk_size = SAMPLE_RATE * 2  # 1 second chunks
        for i in range(0, len(silence), chunk_size):
            chunk = silence[i:i+chunk_size]
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
        await stream.input_stream.end_stream()
        print("✅ Audio sent, stream ended")

    await asyncio.gather(send_audio(), handler.handle_events())
    
    total_time = time.time() - start
    transcript = " ".join(transcript_parts).strip()
    print(f"\n📝 Final transcript: '{transcript}'")
    print(f"⏱️ Total time: {total_time:.2f}s")
    return transcript


def test_with_real_audio():
    """Test with a real audio file if available."""
    test_files = [
        '/tmp/test_audio.webm',
        '/tmp/test_audio.wav',
    ]
    
    for f in test_files:
        if os.path.exists(f):
            print(f"\n🎤 Testing with real audio: {f}")
            with open(f, 'rb') as fh:
                audio_bytes = fh.read()
            audio_b64 = base64.b64encode(audio_bytes).decode()
            
            from transcribe_stt import transcribe_audio
            start = time.time()
            result = transcribe_audio(audio_b64, "test-session")
            elapsed = time.time() - start
            print(f"📝 Result: '{result}'")
            print(f"⏱️ Time: {elapsed:.2f}s")
            return


if __name__ == '__main__':
    print("=" * 60)
    print("🧪 TRANSCRIBE STREAMING TEST")
    print("=" * 60)
    
    print("\n--- Test 1: Streaming API connectivity ---")
    try:
        asyncio.run(test_streaming())
        print("✅ Streaming API works!")
    except Exception as e:
        print(f"❌ Streaming failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n--- Test 2: Real audio (if available) ---")
    test_with_real_audio()
