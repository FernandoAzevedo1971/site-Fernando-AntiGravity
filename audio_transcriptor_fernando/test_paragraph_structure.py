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
print(f"Testing with: {test_file}\n")

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
    
    response = client.listen.v1.media.transcribe_file(request=buffer_data, **options)
    
    # Access paragraphs
    paragraphs = response.results.channels[0].alternatives[0].paragraphs
    
    if paragraphs and hasattr(paragraphs, 'paragraphs'):
        print(f"Total paragraphs: {len(paragraphs.paragraphs)}\n")
        
        # Check first paragraph structure
        first_para = paragraphs.paragraphs[0]
        print(f"First paragraph speaker: {first_para.speaker}")
        print(f"Has 'text' attribute: {hasattr(first_para, 'text')}")
        print(f"Has 'sentences' attribute: {hasattr(first_para, 'sentences')}")
        
        if hasattr(first_para, 'sentences'):
            print(f"\nNumber of sentences: {len(first_para.sentences)}")
            
            if len(first_para.sentences) > 0:
                first_sentence = first_para.sentences[0]
                print(f"\nFirst sentence attributes: {dir(first_sentence)}")
                print(f"Has 'text': {hasattr(first_sentence, 'text')}")
                
                if hasattr(first_sentence, 'text'):
                    print(f"Sentence text: {first_sentence.text}")
        
        # Try to reconstruct text from sentences
        print("\n" + "="*80)
        print("FORMATTED OUTPUT WITH DIARIZATION:")
        print("="*80 + "\n")
        
        for para in paragraphs.paragraphs:
            speaker = para.speaker
            
            # Reconstruct text from sentences
            if hasattr(para, 'sentences'):
                text = " ".join([s.text for s in para.sentences if hasattr(s, 'text')])
                print(f"Speaker {int(speaker)}: {text}\n")
            else:
                print(f"Speaker {int(speaker)}: [no sentences]\n")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
