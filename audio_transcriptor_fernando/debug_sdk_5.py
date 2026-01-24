import os
import inspect
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=api_key)
    # We found the path is client.listen.v1.media.transcribe_file
    method = client.listen.v1.media.transcribe_file
    
    print(f"Method: {method}")
    print(f"Signature: {inspect.signature(method)}")
    print(f"Docstring: {method.__doc__}")

except Exception as e:
    print(f"Error: {e}")
