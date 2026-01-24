import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing correct balance API method...\n")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # Get project
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"Project ID: {project_id}")
    
    # Try using balances directly (not list_balances)
    print("\n--- Getting balances via billing.balances ---")
    try:
        balances = client.manage.v1.projects.billing.balances.list(project_id=project_id)
        print(f"✓ SUCCESS! Balances response type: {type(balances)}")
        print(f"Balances attributes: {dir(balances)}")
        
        if hasattr(balances, 'balances'):
            print(f"\n✓ Has 'balances' attribute")
            print(f"Number of balances: {len(balances.balances)}")
            
            if len(balances.balances) > 0:
                for i, balance in enumerate(balances.balances):
                    print(f"\n--- Balance {i+1} ---")
                    print(f"Balance object: {balance}")
                    print(f"Balance attributes: {dir(balance)}")
                    
                    if hasattr(balance, 'balance_id'):
                        print(f"  Balance ID: {balance.balance_id}")
                    if hasattr(balance, 'amount'):
                        print(f"  Amount: {balance.amount}")
                    if hasattr(balance, 'units'):
                        print(f"  Units: {balance.units}")
                    if hasattr(balance, 'purchase_order_id'):
                        print(f"  Purchase Order ID: {balance.purchase_order_id}")
        else:
            print("No 'balances' attribute found")
            print(f"Full response: {balances}")
            
    except Exception as e:
        print(f"Error with balances.list: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
