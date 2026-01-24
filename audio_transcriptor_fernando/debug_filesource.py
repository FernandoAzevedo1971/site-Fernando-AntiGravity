import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, FileSource

load_dotenv(override=True)
api_key = os.getenv("DEEPGRAM_API_KEY")

try:
    # Test what FileSource looks like and how to create it
    print(f"FileSource type: {FileSource}")
    print(f"FileSource attributes: {dir(FileSource)}")
    
    # Try creating a test FileSource
    test_data = b"fake audio data"
    
    # Check different ways to create it
    print("\nTrying different FileSource creation methods:")
    
    # Method 1: Direct dict (what we're doing now - likely wrong)
    method1 = {"buffer": test_data}
    print(f"Method 1 (dict): {type(method1)}")
    
    # Method 2: FileSource class
    try:
        method2 = FileSource(buffer=test_data)
        print(f"Method 2 (FileSource with buffer kwarg): {type(method2)}")
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    # Method 3: FileSource from buffer
    try:
        method3 = FileSource.from_buffer(test_data)
        print(f"Method 3 (FileSource.from_buffer): {type(method3)}")
    except Exception as e:
        print(f"Method 3 failed: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
