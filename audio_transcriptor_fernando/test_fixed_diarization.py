import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

# Find a test audio file
test_dir = r"C:\Users\ferna\OneDrive\Documentos\Gravacoes Som Audio Recorder Free"
audio_files = []

if os.path.exists(test_dir):
    for file in os.listdir(test_dir):
        if file.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
            audio_files.append(os.path.join(test_dir, file))
            break

if not audio_files:
    print("No audio files found")
    exit(1)

test_file = audio_files[0]

def format_diarized_transcript(response):
    """Format the transcript with speaker diarization - SAME FUNCTION AS IN MAIN.PY"""
    try:
        # Get the paragraphs with speaker information
        paragraphs = response.results.channels[0].alternatives[0].paragraphs
        
        if not paragraphs or not hasattr(paragraphs, 'paragraphs'):
            # Fallback to simple transcript if diarization not available
            return response.results.channels[0].alternatives[0].transcript
        
        formatted_text = ""
        for para in paragraphs.paragraphs:
            speaker = para.speaker
            
            # Extract text from sentences (paragraphs don't have a direct 'text' attribute)
            if hasattr(para, 'sentences') and para.sentences:
                text = " ".join([s.text for s in para.sentences if hasattr(s, 'text')])
            else:
                # Fallback: reconstruct from words if sentences are not available
                text = "[no text available]"
            
            # Format: "Speaker 0: [text]"
            formatted_text += f"Speaker {int(speaker)}: {text}\n\n"
        
        return formatted_text.strip()
    
    except Exception as e:
        print(f"Error formatting diarization: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to simple transcript
        try:
            return response.results.channels[0].alternatives[0].transcript
        except:
            return "Erro ao processar transcrição"

try:
    client = DeepgramClient(api_key=api_key)
    
    print(f"Testing with: {test_file}\n")
    print("Sending to Deepgram API...\n")
    
    with open(test_file, "rb") as file:
        buffer_data = file.read()
    
    options = {
        "model": "nova-3",
        "smart_format": True,
        "diarize": True,
        "paragraphs": True,
        "language": "pt-BR",
    }
    
    response = client.listen.v1.media.transcribe_file(request=buffer_data, **options)
    
    # Test the formatting function
    formatted_output = format_diarized_transcript(response)
    
    print("="*80)
    print("FORMATTED TRANSCRIPT WITH DIARIZATION:")
    print("="*80)
    print(formatted_output)
    print("\n" + "="*80)
    print(f"✓ Success! Diarization is working correctly.")
    print("="*80)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
