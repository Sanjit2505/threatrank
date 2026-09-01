# Cyber Incident Response System (ThreatRank AI)

An enterprise-grade, real-time cybersecurity incident response platform featuring a Vercel-inspired minimalist dark UI. The platform continuously ingests network telemetry, evaluates threats using an AI priority engine, dynamically assigns tasks to specialized SOC agents, and tracks response progress and impact in real time.

## 🛠️ Technology Stack

### Frontend Architecture
* **React 18** (UI Library) - Utilizing Functional Components, `useState` for state management, `useEffect` for lifecycle hooks, and `useRef` for persistent WebSocket connections.
* **Vite** (Build Tool) - High-performance frontend tooling and hot-module replacement.
* **Vanilla CSS3** - Custom, zero-dependency Vercel-style monochromatic dark theme (`#000000` pitch black). Utilizes CSS Grid (`grid-template-columns`), Flexbox, and CSS Animations (pulsing status dots).
* **HTML5 SVG** - Used for rendering the interactive network topology graph (Asset Nodes) directly in the DOM without heavy charting libraries.
* **WebSockets API** - Native browser API used for real-time, low-latency streaming of backend state updates.

### Backend Architecture
* **Python 3.10+** - Core backend language.
* **FastAPI** - High-performance async web framework used for handling REST endpoints (`/alert`, `/assign`, `/incidents`) and WebSocket connections (`/ws`).
* **Uvicorn** - Lightning-fast ASGI server implementation.
* **Pydantic** - Data validation and settings management (e.g., `ThreatPayload`, `AssignmentRequest`).
* **Asyncio** - Standard Python asynchronous I/O. Crucial for simulating real-world task progression timelines (`await asyncio.sleep(X)`) without blocking the main thread.

### Threat Generation & ML
* **Threading Module** - Python `threading` used in the Threat Generator to simulate 5 concurrent, multi-vector attack streams.
* **Requests** - HTTP library used by the generator to push payloads to the FastAPI ingestion endpoints.

---

## 🐍 Core Python Functions & Modules

### 1. `backend/server.py` (Main Controller)
* **`websocket_endpoint(websocket: WebSocket)`**: Accepts incoming WebSocket connections, adds them to the `active_connections` pool, and pushes the initial system state.
* **`broadcast_state()`**: Serializes the current `incidents`, `engineers`, and `system_activities` lists into JSON and asynchronously pushes the payload to all connected frontend clients.
* **`receive_alert(threat: ThreatPayload)`**: The core REST ingestion endpoint (`POST /alert`). It calculates AI risk scores, maps the threat to target assets, selects the best security engineer, builds the incident object, broadcasts the update, and spawns a background asynchronous task (`simulate_task_lifecycle`).
* **`simulate_task_lifecycle(incident_id: str)`**: An asynchronous loop that progresses a task through stages (`Assigned` $\rightarrow$ `In Progress` $\rightarrow$ `Completed`). It uses `asyncio.sleep()` to simulate real-world mitigation delays, updates the incident's `effect` (Before vs After), and automatically removes the completed task from the active queue after 2 seconds.
* **`pick_best_engineer(attack_type, priority_score)`**: Intelligent routing algorithm that matches the incoming threat profile (e.g., "Data Exfiltration") to the specific specialty of the 12 available engineers (e.g., "Sarah Chen - Cloud Security Specialist"), while respecting their active workload capacity.
* **`update_engineer_counts()`**: Recalculates and synchronizes the active task loads (`assigned_count`) for all engineers based on the current pending incidents in the queue.
* **`add_activity_log(time, message, type)`**: Appends a formatted timestamped log to the `system_activities` array, keeping a maximum rolling buffer of 50 events.

### 2. Analytical Engines (Imported Modules)
* **`ai_predictor.py -> predict_threat(features)`**: Takes raw network telemetry (bytes, packets, failed logins) and classifies the attack vector (e.g., "Brute Force", "Port Scan") while assigning an AI confidence percentage.
* **`priority_engine.py -> calculate_priority(...)`**: A heuristic scoring function that evaluates attack severity, target asset criticality (e.g., Payment Gateway vs. Employee Laptop), and business impact to output a final Priority Score (0-100).
* **`response_engine.py -> get_recommended_action(...)`**: Returns specific, actionable mitigation steps (e.g., "Isolate Host", "Block IP via Firewall") based on the classified threat pattern.

### 3. `threat_generator.py` (Simulation Script)
* **`alert_worker(thread_id)`**: A daemon thread function that continuously generates randomized threat payloads (simulating different attack profiles like Reconnaissance or Data Exfiltration) and `POST`s them to the backend at randomized intervals.
