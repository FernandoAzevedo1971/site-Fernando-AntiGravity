import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=api_key)
    listen = client.listen
    v1 = listen.v1
    
    print(f"v1 keys: {dir(v1)}")
    
    if hasattr(v1, 'transcribe_file'):
        print("FOUND transcribe_file in v1")
    else:
        print("v1 DOES NOT have transcribe_file")
        
except Exception as e:
    print(f"Error: {e}")
