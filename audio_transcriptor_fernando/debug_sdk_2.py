import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=api_key)
    listen = client.listen
    
    print(f"Listen.v('1'): {listen.v('1')}")
    print(f"Listen.v('1') keys: {dir(listen.v('1'))}")

    # Check for transcribe_file
    if hasattr(listen.v('1'), 'transcribe_file'):
        print("FOUND transcribe_file in v('1')")
    
    # Also check 'rest' again just in case v('1') returns something that has it, though unlikely
    
except Exception as e:
    print(f"Error: {e}")
