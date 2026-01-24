import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv(override=True)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Exploring all available Deepgram API endpoints...\n")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # Get project
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"Project ID: {project_id}\n")
    
    # Explore what's available under manage.v1
    print("="*80)
    print("EXPLORING manage.v1 structure")
    print("="*80)
    print(f"\nmanage.v1 attributes:")
    v1_attrs = [attr for attr in dir(client.manage.v1) if not attr.startswith('_')]
    for attr in v1_attrs:
        print(f"  - {attr}")
    
    # Check usage
    if hasattr(client.manage.v1, 'usage'):
        print("\n" + "="*80)
        print("EXPLORING manage.v1.usage")
        print("="*80)
        usage_attrs = [attr for attr in dir(client.manage.v1.usage) if not attr.startswith('_')]
        for attr in usage_attrs:
            print(f"  - {attr}")
        
        # Try to get usage/credits
        print("\n--- Trying to get usage ---")
        try:
            # Try different methods
            if hasattr(client.manage.v1.usage, 'list'):
                print("\nTrying usage.list()...")
                usage = client.manage.v1.usage.list(project_id=project_id)
                print(f"✓ SUCCESS! Usage response: {usage}")
            elif hasattr(client.manage.v1.usage, 'get'):
                print("\nTrying usage.get()...")
                usage = client.manage.v1.usage.get(project_id=project_id)
                print(f"✓ SUCCESS! Usage response: {usage}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Check if there's a separate endpoint for credits/balance without billing scope
    print("\n" + "="*80)
    print("EXPLORING project-level methods")
    print("="*80)
    project_attrs = [attr for attr in dir(client.manage.v1.projects) if not attr.startswith('_')]
    for attr in project_attrs:
        print(f"  - {attr}")
    
    # Try to get project details which might include balance
    print("\n--- Getting project details ---")
    try:
        project_details = client.manage.v1.projects.get(project_id=project_id)
        print(f"✓ Project details type: {type(project_details)}")
        print(f"Project details attributes: {dir(project_details)}")
        print(f"\nProject details: {project_details}")
    except Exception as e:
        print(f"Error: {e}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
