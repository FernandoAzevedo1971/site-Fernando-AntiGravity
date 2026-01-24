import os
from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("Testing Deepgram Balance API - Round 2...")

try:
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    
    # We know manage.v1.projects exists, let's explore it
    print(f"manage.v1.projects attributes: {dir(client.manage.v1.projects)}")
    
    # Try to list projects first
    print("\n--- Listing projects ---")
    try:
        projects = client.manage.v1.projects.list()
        print(f"Projects response type: {type(projects)}")
        print(f"Projects response: {projects}")
        
        if hasattr(projects, 'projects'):
            print(f"\nNumber of projects: {len(projects.projects)}")
            if len(projects.projects) > 0:
                first_project = projects.projects[0]
                print(f"First project: {first_project}")
                print(f"First project attributes: {dir(first_project)}")
                
                if hasattr(first_project, 'project_id'):
                    project_id = first_project.project_id
                    print(f"\nProject ID: {project_id}")
                    
                    # Now try to get balances for this project
                    print("\n--- Getting balances for project ---")
                    try:
                        balances = client.manage.v1.projects.get_balances(project_id=project_id)
                        print(f"Balances response type: {type(balances)}")
                        print(f"Balances response: {balances}")
                        print(f"Balances attributes: {dir(balances)}")
                        
                        if hasattr(balances, 'balances'):
                            print(f"\nNumber of balances: {len(balances.balances)}")
                            if len(balances.balances) > 0:
                                balance = balances.balances[0]
                                print(f"First balance: {balance}")
                                print(f"Balance attributes: {dir(balance)}")
                                
                                if hasattr(balance, 'amount'):
                                    print(f"Amount: {balance.amount}")
                                if hasattr(balance, 'units'):
                                    print(f"Units: {balance.units}")
                    except Exception as e:
                        print(f"Error getting balances: {e}")
                        import traceback
                        traceback.print_exc()
    except Exception as e:
        print(f"Error listing projects: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
