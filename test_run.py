from src.maindb import create_db_and_tables
from src.agent_flow import process_chat_query
import time

print("Creating tables...")
create_db_and_tables()

def run_query(name, query, user_id=1):
    print(f"\nStarting {name}: '{query}'")
    start_time = time.time()
    result = process_chat_query(query, user_id=user_id)
    print(f"Finished {name} in {time.time() - start_time:.2f}s:\n{result}\n")
    time.sleep(3)  # Rate limit buffer between queries
    return result

run_query("Query 1", "add hero Batman with secret name Bruce Wayne and age 35")
run_query("Query 2", "add 3 heroes: Iron Man (secret name Tony Stark, age 45), Thor (secret name Thor Odinson, age 1500), and Captain America (secret name Steve Rogers, age 100)")
run_query("Query 3", "update Batman's age to 40")
run_query("Query 4", "delete Thor")
run_query("Query 5", "add hero Wolverine", 2)
run_query("Query 6", "show heroes")

print("All queries completed.")
