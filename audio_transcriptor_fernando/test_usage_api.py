import os
from dotenv import load_dotenv
from deepgram import DeepgramClient
import datetime

load_dotenv(override=True)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing Deepgram USAGE API...\n")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # Get project
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"Project ID: {project_id}\n")
    
    # Explore usage endpoint
    print("="*80)
    print("EXPLORING projects.usage")
    print("="*80)
    usage_attrs = [attr for attr in dir(client.manage.v1.projects.usage) if not attr.startswith('_')]
    for attr in usage_attrs:
        print(f"  - {attr}")
    
    # Try to get usage without date parameters
    print("\n--- Attempt 1: usage.list() without parameters ---")
    try:
        usage = client.manage.v1.projects.usage.list(project_id=project_id)
        print(f"✓ SUCCESS!")
        print(f"Usage type: {type(usage)}")
        print(f"Usage attributes: {dir(usage)}")
        print(f"Usage: {usage}")
    except Exception as e:
        print(f"Failed: {e}")
    
    # Try with date range (last 30 days)
    print("\n--- Attempt 2: usage.list() with date range ---")
    try:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
        
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        
        print(f"Date range: {start_str} to {end_str}")
        
        usage = client.manage.v1.projects.usage.list(
            project_id=project_id,
            start=start_str,
            end=end_str
        )
        print(f"✓ SUCCESS!")
        print(f"Usage type: {type(usage)}")
        print(f"Usage attributes: {dir(usage)}")
        print(f"\nUsage details:")
        
        if hasattr(usage, 'results'):
            print(f"  Results: {usage.results}")
        if hasattr(usage, 'resolution'):
            print(f"  Resolution: {usage.resolution}")
        if hasattr(usage, 'start'):
            print(f"  Start: {usage.start}")
        if hasattr(usage, 'end'):
            print(f"  End: {usage.end}")
            
        print(f"\nFull usage object: {usage}")
    except Exception as e:
        print(f"Failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Try get method if exists
    if hasattr(client.manage.v1.projects.usage, 'get'):
        print("\n--- Attempt 3: usage.get() ---")
        try:
            usage = client.manage.v1.projects.usage.get(project_id=project_id)
            print(f"✓ SUCCESS! Usage: {usage}")
        except Exception as e:
            print(f"Failed: {e}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
