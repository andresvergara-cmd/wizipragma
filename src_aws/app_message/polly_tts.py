"""
Module: Amazon Polly Text-to-Speech
Synthesizes text responses to natural speech using Amazon Polly Neural voices
"""

import boto3
import base64
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize Polly client
polly = boto3.client('polly', region_name='us-east-1')

# Voice configuration for Comfi
VOICE_ID = 'Mia'  # Spanish (Mexico) - Neural voice, friendly and clear
LANGUAGE_CODE = 'es-MX'
ENGINE = 'neural'  # Neural voices sound more natural
OUTPUT_FORMAT = 'mp3'  # MP3 for web compatibility
SAMPLE_RATE = '24000'  # 24kHz for high quality


def synthesize_speech(text: str, voice_id: str = VOICE_ID) -> dict:
    """
    Synthesize text to speech using Amazon Polly
    
    Args:
        text: Text to synthesize (max 3000 characters for neural voices)
        voice_id: Polly voice ID (default: Mia for es-MX)
        
    Returns:
        dict: {
            'audio_base64': Base64 encoded audio (MP3),
            'content_type': 'audio/mpeg',
            'sample_rate': '24000'
        }
    """
    try:
        logger.info(f"Synthesizing speech with Polly (voice: {voice_id}, text length: {len(text)} chars)")
        
        # Truncate text if too long (neural voices have 3000 char limit)
        if len(text) > 3000:
            logger.warning(f"Text too long ({len(text)} chars), truncating to 3000")
            text = text[:2997] + "..."
        
        # Call Polly to synthesize speech
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat=OUTPUT_FORMAT,
            VoiceId=voice_id,
            Engine=ENGINE,
            LanguageCode=LANGUAGE_CODE,
            SampleRate=SAMPLE_RATE
        )
        
        # Read audio stream
        audio_stream = response['AudioStream'].read()
        logger.info(f"Speech synthesized successfully: {len(audio_stream)} bytes")
        
        # Encode to base64 for transmission
        audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
        
        return {
            'audio_base64': audio_base64,
            'content_type': 'audio/mpeg',
            'sample_rate': SAMPLE_RATE,
            'voice_id': voice_id,
            'size_bytes': len(audio_stream)
        }
        
    except Exception as e:
        logger.error(f"Error synthesizing speech with Polly: {str(e)}")
        raise Exception(f"Speech synthesis failed: {str(e)}")


def synthesize_speech_ssml(ssml_text: str, voice_id: str = VOICE_ID) -> dict:
    """
    Synthesize SSML text to speech for advanced control
    
    SSML allows control over:
    - Pronunciation
    - Pauses
    - Emphasis
    - Speaking rate
    - Pitch
    
    Args:
        ssml_text: SSML formatted text
        voice_id: Polly voice ID
        
    Returns:
        dict: Same as synthesize_speech()
    """
    try:
        logger.info(f"Synthesizing SSML with Polly (voice: {voice_id})")
        
        response = polly.synthesize_speech(
            Text=ssml_text,
            TextType='ssml',
            OutputFormat=OUTPUT_FORMAT,
            VoiceId=voice_id,
            Engine=ENGINE,
            LanguageCode=LANGUAGE_CODE,
            SampleRate=SAMPLE_RATE
        )
        
        audio_stream = response['AudioStream'].read()
        audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
        
        return {
            'audio_base64': audio_base64,
            'content_type': 'audio/mpeg',
            'sample_rate': SAMPLE_RATE,
            'voice_id': voice_id,
            'size_bytes': len(audio_stream)
        }
        
    except Exception as e:
        logger.error(f"Error synthesizing SSML with Polly: {str(e)}")
        raise Exception(f"SSML synthesis failed: {str(e)}")


def get_available_voices(language_code: str = 'es-MX') -> list:
    """
    Get list of available Polly voices for a language
    
    Args:
        language_code: Language code (e.g., 'es-MX', 'es-ES')
        
    Returns:
        list: List of voice dictionaries
    """
    try:
        response = polly.describe_voices(
            LanguageCode=language_code,
            Engine=ENGINE
        )
        
        voices = response.get('Voices', [])
        logger.info(f"Found {len(voices)} voices for {language_code}")
        
        return [
            {
                'id': voice['Id'],
                'name': voice['Name'],
                'gender': voice['Gender'],
                'language': voice['LanguageCode']
            }
            for voice in voices
        ]
        
    except Exception as e:
        logger.error(f"Error getting voices: {str(e)}")
        return []


# Example SSML templates for common scenarios
SSML_TEMPLATES = {
    'greeting': '''<speak>
        <prosody rate="medium" pitch="medium">
            ¡Hola! Soy Comfi, tu asistente de Comfama.
            <break time="300ms"/>
            ¿En qué puedo ayudarte hoy?
        </prosody>
    </speak>''',
    
    'emphasis': '''<speak>
        <prosody rate="medium">
            {text}
            <emphasis level="strong">{emphasized_text}</emphasis>
        </prosody>
    </speak>''',
    
    'slow_explanation': '''<speak>
        <prosody rate="slow" pitch="medium">
            {text}
        </prosody>
    </speak>'''
}


if __name__ == "__main__":
    # Test synthesis
    test_text = "Hola, soy Comfi, tu asistente virtual de Comfama. ¿En qué puedo ayudarte hoy?"
    result = synthesize_speech(test_text)
    print(f"✅ Synthesis successful: {result['size_bytes']} bytes")
    
    # List available voices
    voices = get_available_voices('es-MX')
    print(f"\n📢 Available voices for es-MX:")
    for voice in voices:
        print(f"  - {voice['name']} ({voice['gender']})")
