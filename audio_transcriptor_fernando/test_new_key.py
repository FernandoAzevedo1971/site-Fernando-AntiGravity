import os
import sys
from dotenv import load_dotenv
from deepgram import DeepgramClient

# Force reload of environment variables
for key in list(os.environ.keys()):
    if key.startswith('DEEPGRAM'):
        del os.environ[key]

load_dotenv(override=True)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing NEW OWNER API Key (Force Reload)...\n")
print(f"API Key: {DEEPGRAM_API_KEY}\n")

if not DEEPGRAM_API_KEY or DEEPGRAM_API_KEY.startswith("31c7080"):
    print("✗ ERROR: Still loading old API key!")
    print("Checking .env file directly...")
    with open(".env", "r") as f:
        print(f.read())
    sys.exit(1)

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # Get project
    print("Step 1: Getting project...")
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"✓ Project ID: {project_id}\n")
    
    # Try to get balances
    print("Step 2: Getting balances with OWNER key...")
    balances = client.manage.v1.projects.billing.balances.list(project_id=project_id)
    
    print(f"✓ SUCCESS! Got balances response")
    
    if hasattr(balances, 'balances') and balances.balances:
        print(f"✓ Number of balances: {len(balances.balances)}")
        
        total = 0
        for balance in balances.balances:
            if hasattr(balance, 'amount'):
                total += balance.amount
        
        print(f"\n{'='*60}")
        print(f"✓✓✓ TOTAL BALANCE: ${total:.2f} ✓✓✓")
        print(f"{'='*60}")
        print(f"\n🎉 SUCCESS! The Owner API key works perfectly!")
        print(f"The app will now show: 'Saldo: ${total:.2f}' in green\n")
    else:
        print("No balances found")
        
except Exception as e:
    print(f"✗ Error: {e}")
    if "billing:read" in str(e):
        print("\n⚠️ The API key still doesn't have billing:read permissions!")
        print("Please verify:")
        print("1. The API key was created with 'Owner' role (not Admin)")
        print("2. You copied the correct key")
