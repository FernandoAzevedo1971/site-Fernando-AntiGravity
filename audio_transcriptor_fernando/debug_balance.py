import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing Deepgram Balance API...")
print(f"API Key exists: {bool(DEEPGRAM_API_KEY)}")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    print(f"Client created successfully")
    
    # Check if manage.v1 exists
    print(f"\nClient attributes: {dir(client)}")
    
    if hasattr(client, 'manage'):
        print(f"\nManage object exists")
        print(f"Manage attributes: {dir(client.manage)}")
        
        if hasattr(client.manage, 'v1'):
            print(f"\nManage.v1 exists")
            print(f"Manage.v1 attributes: {dir(client.manage.v1)}")
            
            # Try to get balances
            try:
                # First, check if we need project_id
                if hasattr(client, 'config'):
                    print(f"\nClient.config exists")
                    print(f"Config attributes: {dir(client.config)}")
                    if hasattr(client.config, 'project_id'):
                        print(f"Project ID: {client.config.project_id}")
                
                # Try different approaches
                print("\n--- Attempting to get balances ---")
                
                # Approach 1: With project_id
                try:
                    response = client.manage.v1.get_balances(project_id=client.config.project_id)
                    print(f"Approach 1 (with project_id) SUCCESS: {response}")
                except Exception as e:
                    print(f"Approach 1 (with project_id) FAILED: {e}")
                
                # Approach 2: Without project_id
                try:
                    response = client.manage.v1.get_balances()
                    print(f"Approach 2 (without project_id) SUCCESS: {response}")
                except Exception as e:
                    print(f"Approach 2 (without project_id) FAILED: {e}")
                    
            except Exception as e:
                print(f"Error calling get_balances: {e}")
        else:
            print("Manage.v1 does NOT exist")
    else:
        print("Manage object does NOT exist")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
