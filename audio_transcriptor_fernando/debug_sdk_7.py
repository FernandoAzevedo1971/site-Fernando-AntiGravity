import os
import inspect
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=api_key)
    method = client.listen.v1.media.transcribe_file
    
    sig = inspect.signature(method)
    params = list(sig.parameters.keys())
    print(f"Parameter names: {params}")
    
    full_spec = inspect.getfullargspec(method)
    print(f"Full Arg Spec: {full_spec}")

except Exception as e:
    print(f"Error: {e}")
