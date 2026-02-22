import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

# trial script

API_URL = "http://127.0.0.1:8000/ticket"  
TOTAL_TICKETS = 20
MAX_WORKERS = 5  

# Mock Data for Variation
SUBJECTS = ["Server Down", "Payment Failed", "Login Loop", "Database Error", "UI Bug"]
BODIES = [
    "I can't access my dashboard, it's urgent!",
    "The invoice #1234 is showing the wrong amount.",
    "Getting a 500 error on the login page.",
    "System is slow and unresponsive since morning.",
    "The 'Submit' button isn't clicking on Chrome.",
]
TYPES = ["request", "bug", "incident"]
TAGS = ["urgent", "v1-prod", "customer-tier-1", "bug", "feature-req", None]


def generate_mock_ticket():
    """Generates a random ticket matching the TicketRequest model."""
    return {
        "subject": random.choice(SUBJECTS),
        "body": random.choice(BODIES),
        "type": random.choice(TYPES),
        "tag1": random.choice(TAGS),
        "tag2": random.choice(TAGS),
        "tag3": random.choice(TAGS),
    }


def send_ticket(ticket_index):
    """Sends a single POST request to the engine."""
    payload = generate_mock_ticket()
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 202:
            data = response.json()
            print(
                f"[{ticket_index}] Success! ID: {data.get('ticket_id')} | Status: {data.get('status')}"
            )
        else:
            print(
                f"[ {ticket_index}] Failed! Status: {response.status_code} | Error: {response.text}"
            )
    except Exception as e:
        print(f"[{ticket_index}] Connection Error: {e}")


def run_simulation():
    print(f"Starting Simulation: Sending {TOTAL_TICKETS} tickets to {API_URL}...")
    start_time = time.time()

    # Using ThreadPoolExecutor to simulate multiple users hitting the API at once
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(send_ticket, range(1, TOTAL_TICKETS + 1))

    end_time = time.time()
    print(f"\nSimulation Finished in {round(end_time - start_time, 2)} seconds.")


def send_single_ticket(index: int):
 
    payload = generate_mock_ticket()
    print(f"--- Sending Ticket #{index} ---")

    try:
        response = requests.post(API_URL, json=payload, timeout=5)

        if response.status_code == 202:
            data = response.json()
            print(
                f"Success | ID: {data.get('ticket_id')} | Status: {data.get('status')}"
            )
        else:
            print(
                f"Failed  | Status: {response.status_code} | Error: {response.text}"
            )

    except Exception as e:
        print(f"Connection Error: {e}")


def run_sequential_simulation(count: int, delay: float = 1.0):
    """
    Sends tickets one-by-one with a specific time delay.
    """
    print(f"Starting Sequential Feed: {count} tickets with {delay}s delay...")
    for i in range(1, count + 1):
        send_single_ticket(i)
        time.sleep(delay)


if __name__ == "__main__":
    run_simulation()  
    # run_sequential_simulation(count=5, delay=2.0)  # Example of sequential feed with delay
    # env file to configure router,classifier,storage options for future iterations
