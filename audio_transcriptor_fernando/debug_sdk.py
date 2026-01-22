import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=api_key)
    print(f"Client keys: {dir(client)}")
    
    listen = client.listen
    print(f"Listen keys: {dir(listen)}")
    
    if hasattr(listen, 'prerecorded'):
        print("Listen has 'prerecorded'")
    else:
        print("Listen DOES NOT have 'prerecorded'")
        
    if hasattr(listen, 'rest'):
        print("Listen has 'rest'")
    else:
        print("Listen DOES NOT have 'rest'")

except Exception as e:
    print(f"Error: {e}")
