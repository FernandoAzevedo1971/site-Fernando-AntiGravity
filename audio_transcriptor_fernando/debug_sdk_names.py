import os
import inspect
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=api_key)
    method = client.listen.v1.media.transcribe_file
    
    # Print clean list of names
    print(list(inspect.signature(method).parameters.keys()))

except Exception as e:
    print(f"Error: {e}")
