import os
import json
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv(override=True)
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
    print("No audio files found in the directory")
    exit(1)

test_file = audio_files[0]
print(f"Testing with file: {test_file}\n")

try:
    client = DeepgramClient(api_key=api_key)
    
    with open(test_file, "rb") as file:
        buffer_data = file.read()
    
    options = {
        "model": "nova-3",
        "smart_format": True,
        "diarize": True,
        "paragraphs": True,
        "language": "pt-BR",
    }
    
    print("Sending request to Deepgram...")
    response = client.listen.v1.media.transcribe_file(request=buffer_data, **options)
    
    print("\n" + "="*80)
    print("RESPONSE STRUCTURE:")
    print("="*80)
    
    # Check if diarization data exists
    print(f"\nHas results: {hasattr(response, 'results')}")
    print(f"Has channels: {hasattr(response.results, 'channels')}")
    
    if hasattr(response.results, 'channels') and len(response.results.channels) > 0:
        channel = response.results.channels[0]
        print(f"Has alternatives: {hasattr(channel, 'alternatives')}")
        
        if hasattr(channel, 'alternatives') and len(channel.alternatives) > 0:
            alternative = channel.alternatives[0]
            print(f"Has paragraphs: {hasattr(alternative, 'paragraphs')}")
            print(f"Has transcript: {hasattr(alternative, 'transcript')}")
            print(f"Has words: {hasattr(alternative, 'words')}")
            
            # Check paragraphs structure
            if hasattr(alternative, 'paragraphs'):
                paragraphs = alternative.paragraphs
                print(f"\nParagraphs type: {type(paragraphs)}")
                print(f"Paragraphs dir: {dir(paragraphs)}")
                
                if hasattr(paragraphs, 'paragraphs'):
                    print(f"\nNumber of paragraphs: {len(paragraphs.paragraphs)}")
                    
                    # Show first paragraph
                    if len(paragraphs.paragraphs) > 0:
                        first_para = paragraphs.paragraphs[0]
                        print(f"\nFirst paragraph attributes: {dir(first_para)}")
                        print(f"Has speaker: {hasattr(first_para, 'speaker')}")
                        print(f"Has text: {hasattr(first_para, 'text')}")
                        
                        if hasattr(first_para, 'speaker'):
                            print(f"\nSpeaker: {first_para.speaker}")
                        if hasattr(first_para, 'text'):
                            print(f"Text preview: {first_para.text[:100]}...")
                else:
                    print("\nNo 'paragraphs' attribute in paragraphs object")
            
            # Check words for speaker info
            if hasattr(alternative, 'words') and len(alternative.words) > 0:
                first_word = alternative.words[0]
                print(f"\nFirst word attributes: {dir(first_word)}")
                print(f"First word has speaker: {hasattr(first_word, 'speaker')}")
                if hasattr(first_word, 'speaker'):
                    print(f"First word speaker: {first_word.speaker}")
    
    print("\n" + "="*80)
    print("TRANSCRIPT:")
    print("="*80)
    print(response.results.channels[0].alternatives[0].transcript[:500])
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
