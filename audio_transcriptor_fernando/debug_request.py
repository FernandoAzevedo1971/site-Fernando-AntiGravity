import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, ListenV1RequestFile

load_dotenv()
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    print(f"ListenV1RequestFile: {ListenV1RequestFile}")
    
    # Try creating with test data
    test_data = b"fake audio data"
    
    # Try different initialization methods
    try:
        request1 = ListenV1RequestFile(buffer=test_data)
        print(f"Method 1 (buffer kwarg): {type(request1)}")
        print(f"Request1: {request1}")
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    try:
        request2 = ListenV1RequestFile(content=test_data)
        print(f"Method 2 (content kwarg): {type(request2)}")
        print(f"Request2: {request2}")
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    # Check constructor signature
    import inspect
    print(f"\nConstructor signature: {inspect.signature(ListenV1RequestFile.__init__)}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
