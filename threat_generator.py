import requests
import time
import random
import threading

SERVER_URL = "http://127.0.0.1:8000/alert"

# Realistic-looking threat patterns corresponding to features:
# duration, src_bytes, dst_bytes, failed_logins, login_attempts, src_pkts, dst_pkts

THREAT_PROFILES = [
    {
        "name": "Brute Force / Credential Stuffing",
        "features": lambda: {
            "duration": random.uniform(5, 60),
            "src_bytes": random.uniform(1000, 5000),
            "dst_bytes": random.uniform(500, 2000),
            "failed_logins": random.randint(50, 200),
            "login_attempts": random.randint(60, 250),
            "src_pkts": random.randint(10, 50),
            "dst_pkts": random.randint(10, 50),
            "severity": random.randint(7, 9),
            "asset_criticality": random.randint(6, 10),
            "business_impact": random.randint(6, 9),
            "affected_users": random.randint(1, 5)
        }
    },
    {
        "name": "Data Exfiltration",
        "features": lambda: {
            "duration": random.uniform(100, 500),
            "src_bytes": random.uniform(100000, 5000000),
            "dst_bytes": random.uniform(500, 1000),
            "failed_logins": 0,
            "login_attempts": 1,
            "src_pkts": random.randint(500, 2000),
            "dst_pkts": random.randint(10, 50),
            "severity": random.randint(8, 10),
            "asset_criticality": random.randint(8, 10),
            "business_impact": random.randint(9, 10),
            "affected_users": random.randint(10, 100)
        }
    },
    {
        "name": "Port Scan / Reconnaissance",
        "features": lambda: {
            "duration": random.uniform(0.1, 2),
            "src_bytes": random.uniform(5000, 20000),
            "dst_bytes": random.uniform(0, 500),
            "failed_logins": 0,
            "login_attempts": 0,
            "src_pkts": random.randint(100, 500),
            "dst_pkts": random.randint(0, 10),
            "severity": random.randint(3, 5),
            "asset_criticality": random.randint(4, 7),
            "business_impact": random.randint(2, 5),
            "affected_users": 0
        }
    },
    {
        "name": "Normal Traffic",
        "features": lambda: {
            "duration": random.uniform(1, 10),
            "src_bytes": random.uniform(100, 1000),
            "dst_bytes": random.uniform(1000, 5000),
            "failed_logins": 0,
            "login_attempts": random.randint(0, 1),
            "src_pkts": random.randint(5, 20),
            "dst_pkts": random.randint(5, 20),
            "severity": random.randint(1, 2),
            "asset_criticality": random.randint(1, 5),
            "business_impact": random.randint(1, 2),
            "affected_users": random.randint(1, 2)
        }
    }
]

print("Started Live Threat Generator...")
print(f"Sending alerts to {SERVER_URL}")

# --- Multithreaded alert generation ---
stop_event = threading.Event()
NUM_THREADS = 5  # Adjust this number to control concurrency

def alert_worker(thread_id: int):
    """Continuously generate and send alerts until stopped."""
    while not stop_event.is_set():
        profile = random.choice(THREAT_PROFILES)
        payload = profile["features"]()
        print(f"[Thread {thread_id}] Generating Alert -> Simulating: {profile['name']}")
        try:
            response = requests.post(SERVER_URL, json=payload)
            if response.status_code == 200:
                print(f"[Thread {thread_id}] Alert sent successfully!")
            else:
                print(f"[Thread {thread_id}] Failed to send alert: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[Thread {thread_id}] Server is offline. Ensure the backend is running.")
        time.sleep(random.uniform(3, 8))

threads = []
try:
    for i in range(1, NUM_THREADS + 1):
        t = threading.Thread(target=alert_worker, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    # Keep the main thread alive while workers run
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Keyboard interrupt received. Stopping all threads...")
    stop_event.set()
    for t in threads:
        t.join()
    print("Generator stopped.")
