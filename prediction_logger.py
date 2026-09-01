import random
import threading
import time

# Simple heuristic based prediction function
def predict_threat(payload: dict) -> str:
    """Return a human‑readable prediction based on payload features.
    This mimics an AI model's decision making using rule‑based logic.
    """
    # Example heuristics
    if payload.get('failed_logins', 0) > 30:
        return "Brute Force / Credential Stuffing detected (high failed logins)"
    if payload.get('src_bytes', 0) > 1_000_000:
        return "Data Exfiltration likely (large outbound traffic)"
    if payload.get('src_pkts', 0) > 400:
        return "Port Scan / Reconnaissance activity (many source packets)"
    return "Normal traffic"

# Simulated payload generators matching the profiles from threat_generator
THREAT_PROFILES = [
    lambda: {"failed_logins": random.randint(50, 200), "src_bytes": random.uniform(1000, 5000)},
    lambda: {"failed_logins": 0, "src_bytes": random.uniform(100_000, 5_000_000)},
    lambda: {"failed_logins": 0, "src_pkts": random.randint(500, 2000)},
    lambda: {"failed_logins": 0, "src_bytes": random.uniform(100, 1000)}
]

stop_event = threading.Event()
NUM_THREADS = 3  # Number of concurrent prediction workers

def worker(thread_id: int):
    """Continuously generate payloads, run prediction, and print results."""
    while not stop_event.is_set():
        profile_fn = random.choice(THREAT_PROFILES)
        payload = profile_fn()
        prediction = predict_threat(payload)
        print(f"[Thread {thread_id}] Prediction: {prediction}")
        time.sleep(random.uniform(2, 5))

threads = []
try:
    for i in range(1, NUM_THREADS + 1):
        t = threading.Thread(target=worker, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    # Keep main thread alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping prediction logger…")
    stop_event.set()
    for t in threads:
        t.join()
    print("Logger stopped.")
