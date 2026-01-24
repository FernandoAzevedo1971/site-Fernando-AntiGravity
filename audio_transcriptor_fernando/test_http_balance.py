import os
import requests
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing Direct HTTP API Call for Balance...\n")

try:
    # First get project ID using SDK
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    projects = client.manage.v1.projects.list()
    project_id = projects.projects[0].project_id
    print(f"Project ID: {project_id}\n")
    
    # Try direct HTTP request to balances endpoint
    print("="*80)
    print("Attempting direct HTTP GET request...")
    print("="*80)
    
    url = f"https://api.deepgram.com/v1/projects/{project_id}/balances"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"URL: {url}")
    print(f"Headers: Authorization: Token {DEEPGRAM_API_KEY[:10]}...")
    
    response = requests.get(url, headers=headers)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ SUCCESS! Got balance data:")
        print(f"Data: {data}")
        
        if 'balances' in data:
            total = sum(b.get('amount', 0) for b in data['balances'])
            print(f"\n✓ Total Balance: ${total:.2f}")
    elif response.status_code == 403:
        print(f"\n✗ Permission denied (same as SDK)")
    else:
        print(f"\n✗ Request failed")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
