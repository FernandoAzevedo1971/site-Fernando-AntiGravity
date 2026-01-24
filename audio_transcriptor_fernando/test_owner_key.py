import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv(override=True)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing NEW OWNER API Key for Balance...\n")
print(f"API Key: {DEEPGRAM_API_KEY[:10]}...\n")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # Get project
    print("Step 1: Getting project...")
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"✓ Project ID: {project_id}\n")
    
    # Try to get balances
    print("Step 2: Getting balances...")
    balances = client.manage.v1.projects.billing.balances.list(project_id=project_id)
    
    print(f"✓ SUCCESS! Got balances response")
    print(f"Response type: {type(balances)}")
    
    if hasattr(balances, 'balances') and balances.balances:
        print(f"\n✓ Number of balances: {len(balances.balances)}")
        
        total = 0
        for i, balance in enumerate(balances.balances):
            print(f"\n--- Balance {i+1} ---")
            if hasattr(balance, 'balance_id'):
                print(f"  Balance ID: {balance.balance_id}")
            if hasattr(balance, 'amount'):
                print(f"  Amount: ${balance.amount}")
                total += balance.amount
            if hasattr(balance, 'units'):
                print(f"  Units: {balance.units}")
        
        print(f"\n{'='*60}")
        print(f"✓ TOTAL BALANCE: ${total:.2f}")
        print(f"{'='*60}")
        print(f"\n🎉 SUCCESS! The Owner API key works perfectly!")
        print(f"The app will now show: 'Saldo: ${total:.2f}' in green")
    else:
        print("No balances found in response")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
