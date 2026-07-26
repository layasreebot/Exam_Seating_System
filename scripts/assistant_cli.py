import os
import sys

# Ensure script directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant_engine import ExamAssistantEngine

# ANSI colors for styling
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_cli():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Color.HEADER}{Color.BOLD}================================================================{Color.END}")
    print(f"{Color.CYAN}{Color.BOLD}         EXAM SEATING & DUTY REGISTER QUERY ASSISTANT           {Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}================================================================{Color.END}")
    print("Loading seating and duty records dataset...")
    
    try:
        engine = ExamAssistantEngine()
        print(f"{Color.GREEN}Dataset loaded successfully! Total records: {len(engine.records)}{Color.END}\n")
    except Exception as e:
        print(f"{Color.FAIL}Error loading dataset: {e}{Color.END}")
        sys.exit(1)
        
    while True:
        print(f"{Color.BOLD}Step 1: Identify Yourself{Color.END}")
        print("Please enter your Student ID (e.g., STU105) or Invigilator Name (e.g., Dr. Ashwini Sekar).")
        identity = input(f"{Color.BLUE}Login ID/Name >> {Color.END}").strip()
        
        if identity.lower() == 'exit':
            print("Exiting. Goodbye!")
            break
            
        role, matched_id = engine.identify_user(identity)
        
        if not role:
            print(f"{Color.FAIL}Error: Identity not recognized.{Color.END}")
            suggestions = engine.get_similar_identities(identity)
            if suggestions:
                print(f"{Color.WARNING}Did you mean one of these?{Color.END}")
                for s in suggestions:
                    print(f"  - {s}")
            print()
            continue
            
        print(f"\n{Color.GREEN}Welcome back, {matched_id}! (Role: {role}){Color.END}")
        print(f"Type your question in plain English, or type {Color.BOLD}'logout'{Color.END} to change user.")
        print("-" * 50)
        
        while True:
            query = input(f"{Color.CYAN}{matched_id} >> {Color.END}").strip()
            
            if not query:
                continue
                
            if query.lower() == 'logout':
                print(f"{Color.BLUE}Logged out of {matched_id}.\n{Color.END}")
                break
                
            if query.lower() == 'exit':
                print("Exiting. Goodbye!")
                sys.exit(0)
                
            success, response = engine.answer_query(role, matched_id, query)
            
            if success:
                print(f"\n{Color.GREEN}{Color.BOLD}Answer:{Color.END}")
                print(f"{response}\n")
            else:
                print(f"\n{Color.WARNING}{Color.BOLD}Assistant:{Color.END}")
                print(f"{response}\n")
                
if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
