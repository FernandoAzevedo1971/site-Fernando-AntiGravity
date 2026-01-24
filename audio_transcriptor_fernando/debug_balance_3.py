import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing Deepgram Balance API - Round 3 (billing)...")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # Get project
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"Project ID: {project_id}")
    
    # Check billing attribute
    print(f"\nmanage.v1.projects.billing attributes: {dir(client.manage.v1.projects.billing)}")
    
    # Try to get balances via billing
    print("\n--- Getting balances via billing ---")
    try:
        balances = client.manage.v1.projects.billing.list_balances(project_id=project_id)
        print(f"SUCCESS! Balances response type: {type(balances)}")
        print(f"Balances response: {balances}")
        print(f"Balances attributes: {dir(balances)}")
        
        if hasattr(balances, 'balances'):
            print(f"\nNumber of balances: {len(balances.balances)}")
            if len(balances.balances) > 0:
                balance = balances.balances[0]
                print(f"First balance: {balance}")
                
                if hasattr(balance, 'amount'):
                    print(f"Amount: {balance.amount}")
                if hasattr(balance, 'units'):
                    print(f"Units: {balance.units}")
    except Exception as e:
        print(f"Error with list_balances: {e}")
        
        # Try alternative method names
        print("\nTrying alternative methods...")
        billing_methods = [m for m in dir(client.manage.v1.projects.billing) if not m.startswith('_')]
        print(f"Available billing methods: {billing_methods}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
