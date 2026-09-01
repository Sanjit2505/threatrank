from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from datetime import datetime
import json
import random

from ai_predictor import predict_threat
from priority_engine import calculate_priority, sort_incidents
from response_engine import get_recommended_action

app = FastAPI(title="Live Cyber Incident Response Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

incidents = []
active_connections = []
system_activities = []
history_log = []

# Expanded Team Roster with 12 Security Team Members
ENGINEERS = [
    {"id": "eng_1", "name": "Alex Rivera", "role": "Lead Incident Responder", "max_capacity": 5, "assigned_count": 0, "specialty": "Brute Force & Critical Breach"},
    {"id": "eng_2", "name": "Automated AI Sentinel 01", "role": "Autonomous Response Bot", "max_capacity": 15, "assigned_count": 0, "specialty": "Reconnaissance & Auto Triage"},
    {"id": "eng_3", "name": "Sarah Chen", "role": "Cloud Security Specialist", "max_capacity": 4, "assigned_count": 0, "specialty": "Data Exfiltration & S3 Security"},
    {"id": "eng_4", "name": "Marcus Vance", "role": "Network & Firewall Analyst", "max_capacity": 4, "assigned_count": 0, "specialty": "Port Scan & DDoS Mitigation"},
    {"id": "eng_5", "name": "Elena Rostova", "role": "Active Directory Lead", "max_capacity": 4, "assigned_count": 0, "specialty": "Identity & Credential Stuffing"},
    {"id": "eng_6", "name": "David Kim", "role": "Database Security Engineer", "max_capacity": 4, "assigned_count": 0, "specialty": "Database Injection & Data Leakage"},
    {"id": "eng_7", "name": "Priya Patel", "role": "SOC Tier-2 Specialist", "max_capacity": 5, "assigned_count": 0, "specialty": "General Threat Mitigation"},
    {"id": "eng_8", "name": "James O'Connor", "role": "Threat Intelligence Analyst", "max_capacity": 4, "assigned_count": 0, "specialty": "Advanced Persistent Threat (APT)"},
    {"id": "eng_9", "name": "Kaito Tanaka", "role": "Zero-Day Vulnerability Researcher", "max_capacity": 3, "assigned_count": 0, "specialty": "Kernel Exploits & Reverse Eng"},
    {"id": "eng_10", "name": "Sophia Martinez", "role": "Malware & Forensics Lead", "max_capacity": 4, "assigned_count": 0, "specialty": "Ransomware & Payload Analysis"},
    {"id": "eng_11", "name": "Automated AI Sentinel 02", "role": "Autonomous Isolation Unit", "max_capacity": 15, "assigned_count": 0, "specialty": "Endpoint Quarantining & IP Block"},
    {"id": "eng_12", "name": "Liam Gallagher", "role": "SOC Tier-1 Triage Specialist", "max_capacity": 6, "assigned_count": 0, "specialty": "Initial Alert Verification"}
]

TARGET_ASSETS = [
    {"name": "finance-db-02", "importance": "Very High", "sensitivity": "Very High"},
    {"name": "auth-server-01", "importance": "High", "sensitivity": "High"},
    {"name": "employee-portal", "importance": "Medium", "sensitivity": "Medium"},
    {"name": "payment-gateway-01", "importance": "Critical", "sensitivity": "Very High"},
    {"name": "api-edge-router", "importance": "High", "sensitivity": "Medium"},
    {"name": "customer-data-vault", "importance": "Critical", "sensitivity": "Very High"},
    {"name": "cloud-k8s-cluster", "importance": "High", "sensitivity": "High"}
]

class ThreatPayload(BaseModel):
    duration: float = 5.0
    src_bytes: float = 1200.0
    dst_bytes: float = 800.0
    failed_logins: float = 10.0
    login_attempts: float = 15.0
    src_pkts: float = 50.0
    dst_pkts: float = 40.0
    severity: int = 5
    asset_criticality: int = 5
    business_impact: int = 5
    affected_users: int = 1
    affected_asset_name: str = None

class AssignmentRequest(BaseModel):
    incident_id: str
    engineer_id: str

def add_activity_log(time_str: str, message: str, event_type: str = "info"):
    system_activities.insert(0, {
        "time": time_str,
        "message": message,
        "type": event_type
    })
    if len(system_activities) > 50:
        system_activities.pop()

def update_engineer_counts():
    for eng in ENGINEERS:
        eng["assigned_count"] = 0
    for inc in incidents:
        if inc.get("assigned_engineer"):
            eng_id = inc["assigned_engineer"]["id"]
            eng = next((e for e in ENGINEERS if e["id"] == eng_id), None)
            if eng:
                eng["assigned_count"] += 1

def pick_best_engineer(attack_type: str, priority_score: int):
    """Matches incident to engineer by specialty and current workload."""
    attack_lower = attack_type.lower()
    
    if "brute" in attack_lower or "credential" in attack_lower:
        preferred = ["eng_5", "eng_1", "eng_12", "eng_7"]
    elif "exfiltration" in attack_lower or "leak" in attack_lower or "data" in attack_lower:
        preferred = ["eng_3", "eng_6", "eng_10", "eng_8"]
    elif "scan" in attack_lower or "recon" in attack_lower:
        preferred = ["eng_2", "eng_11", "eng_4"]
    elif priority_score >= 80:
        preferred = ["eng_1", "eng_9", "eng_10", "eng_8"]
    else:
        preferred = ["eng_2", "eng_11", "eng_12", "eng_7"]
        
    for eid in preferred:
        eng = next((e for e in ENGINEERS if e["id"] == eid), None)
        if eng and eng["assigned_count"] < eng["max_capacity"]:
            return eng

    available = [e for e in ENGINEERS if e["assigned_count"] < e["max_capacity"]]
    if available:
        return min(available, key=lambda e: e["assigned_count"])
    return ENGINEERS[1]

async def broadcast_state():
    update_engineer_counts()
    sort_incidents(incidents)
    if not active_connections:
        return
        
    payload = {
        "type": "state_update",
        "incidents": incidents,
        "engineers": ENGINEERS,
        "activities": system_activities,
        "history": history_log
    }
    data = json.dumps(payload)
    for connection in list(active_connections):
        try:
            await connection.send_text(data)
        except:
            if connection in active_connections:
                active_connections.remove(connection)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    update_engineer_counts()
    sort_incidents(incidents)
    payload = {
        "type": "state_update",
        "incidents": incidents,
        "engineers": ENGINEERS,
        "activities": system_activities,
        "history": history_log
    }
    await websocket.send_text(json.dumps(payload))
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)

async def simulate_task_lifecycle(incident_id: str):
    """Simulates live continuous progression of an incident task"""
    await asyncio.sleep(2)
    inc = next((i for i in incidents if i["id"] == incident_id), None)
    if not inc: return

    now = datetime.now().strftime("%H:%M:%S")
    inc["task_status"] = "In Progress"
    inc["status"] = "Investigating"
    inc["timeline"].append({"time": now, "text": f"Investigation started by {inc['assigned_engineer']['name']}"})
    add_activity_log(now, f"Investigation started for {incident_id} by {inc['assigned_engineer']['name']}", "info")
    await broadcast_state()

    await asyncio.sleep(4)
    inc = next((i for i in incidents if i["id"] == incident_id), None)
    if not inc: return

    now = datetime.now().strftime("%H:%M:%S")
    inc["timeline"].append({"time": now, "text": f"Suspicious IP {inc['source_ip']} blocked by firewall rule"})
    add_activity_log(now, f"Suspicious IP {inc['source_ip']} blocked", "warning")
    await broadcast_state()

    await asyncio.sleep(3)
    inc = next((i for i in incidents if i["id"] == incident_id), None)
    if not inc: return

    now = datetime.now().strftime("%H:%M:%S")
    inc["task_status"] = "Completed"
    inc["status"] = "Contained"
    inc["completed_at"] = now
    inc["duration_sec"] = 15
    inc["timeline"].append({"time": now, "text": "Response completed successfully & system monitoring continues"})
    
    inc["effect"]["after"] = {
        "status": "CONTAINED",
        "risk_score": max(10, inc["priority_score"] - 66),
        "traffic": "BLOCKED"
    }

    add_activity_log(now, f"Response completed successfully for {incident_id}", "success")
    await broadcast_state()

    # Wait 2 seconds so the completion is visible, then auto-remove from active queue
    await asyncio.sleep(2)
    if inc in incidents:
        incidents.remove(inc)
        history_log.append(inc)
        add_activity_log(now, f"Task {incident_id} contained & removed from active queue", "success")
        await broadcast_state()

@app.post("/alert")
async def receive_alert(threat: ThreatPayload):
    current_time = datetime.now().strftime("%H:%M:%S")

    features = {
        "duration": threat.duration,
        "src_bytes": threat.src_bytes,
        "dst_bytes": threat.dst_bytes,
        "failed_logins": threat.failed_logins,
        "login_attempts": threat.login_attempts,
        "src_pkts": threat.src_pkts,
        "dst_pkts": threat.dst_pkts
    }

    attack_type, confidence = predict_threat(features)

    priority_score = calculate_priority(
        attack_type, 
        confidence, 
        threat.severity, 
        threat.asset_criticality, 
        threat.business_impact, 
        threat.affected_users
    )

    asset = random.choice(TARGET_ASSETS)
    if threat.affected_asset_name:
        asset["name"] = threat.affected_asset_name

    if priority_score >= 80:
        badge = "CRITICAL"
        title = f"Possible {attack_type.replace('_', ' ').title()}"
    elif priority_score >= 55:
        badge = "HIGH"
        title = f"{attack_type.replace('_', ' ').title()} Attack"
    else:
        badge = "MEDIUM"
        title = f"Suspicious {attack_type.replace('_', ' ').title()}"

    incident_id = f"INC-{2048 + len(incidents)}"
    source_ip = f"{random.randint(100, 199)}.{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    update_engineer_counts()
    assigned_eng = pick_best_engineer(attack_type, priority_score)
    assigned_eng["assigned_count"] += 1

    incident = {
        "id": incident_id,
        "title": title,
        "badge": badge,
        "source_ip": source_ip,
        "target": asset["name"],
        "asset_importance": asset["importance"],
        "data_sensitivity": asset["sensitivity"],
        "affected_users": random.randint(5, 50),
        "detected_time": current_time,
        "status": "Active",
        "priority_score": priority_score,
        "ai_confidence": f"{int(confidence)}%",
        "recommendation": "Immediate Investigation Required" if priority_score >= 70 else "Isolate and Monitor Host",
        "assigned_engineer": {
            "id": assigned_eng["id"],
            "name": assigned_eng["name"],
            "role": assigned_eng["role"]
        },
        "task_title": f"Investigate suspicious {attack_type.replace('_', ' ')} activity",
        "task_priority": "URGENT" if priority_score >= 75 else "HIGH",
        "task_status": "Assigned",
        "timeline": [
            {"time": current_time, "text": "New threat detected"},
            {"time": current_time, "text": f"AI risk score calculated: {priority_score}"},
            {"time": current_time, "text": f"Task automatically assigned to {assigned_eng['name']} ({assigned_eng['role']})"}
        ],
        "completed_at": None,
        "duration_sec": None,
        "effect": {
            "before": {
                "status": "ACTIVE",
                "risk_score": priority_score,
                "traffic": "DETECTED"
            },
            "after": None,
            "details": [
                "[OK] Malicious IP blocked",
                "[OK] Suspicious network connection terminated",
                "[OK] Target database access protected",
                "[OK] Incident risk reduced by 70%",
                "[OK] System monitoring continues"
            ]
        },
        "is_new": True
    }

    incidents.insert(0, incident)
    add_activity_log(current_time, f"New threat received: {incident_id} - {title} -> Assigned to {assigned_eng['name']}", "critical" if badge == "CRITICAL" else "info")
    
    await broadcast_state()

    asyncio.create_task(simulate_task_lifecycle(incident_id))

    return {"message": "Alert processed", "incident": incident}

@app.post("/assign")
async def assign_task(req: AssignmentRequest):
    target_inc = next((i for i in incidents if i["id"] == req.incident_id), None)
    if not target_inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    target_eng = next((e for e in ENGINEERS if e["id"] == req.engineer_id), None)
    if not target_eng:
        raise HTTPException(status_code=404, detail="Engineer not found")

    target_inc["assigned_engineer"] = {
        "id": target_eng["id"],
        "name": target_eng["name"],
        "role": target_eng["role"]
    }
    
    now = datetime.now().strftime("%H:%M:%S")
    target_inc["timeline"].append({"time": now, "text": f"Task manually reassigned to {target_eng['name']} ({target_eng['role']})"})
    add_activity_log(now, f"Task {target_inc['id']} reassigned to {target_eng['name']}", "info")

    await broadcast_state()
    return {"message": "Assigned successfully"}

@app.post("/auto-assign-all")
async def auto_assign_all():
    for inc in incidents:
        if not inc.get("assigned_engineer"):
            eng = pick_best_engineer(inc.get("title", ""), inc.get("priority_score", 50))
            inc["assigned_engineer"] = {"id": eng["id"], "name": eng["name"], "role": eng["role"]}
    await broadcast_state()
    return {"message": "Auto-assigned all pending incidents!"}

@app.get("/incidents")
async def get_incidents():
    return incidents

@app.delete("/incidents")
async def clear_incidents():
    incidents.clear()
    system_activities.clear()
    for eng in ENGINEERS:
        eng["assigned_count"] = 0
    await broadcast_state()
    return {"message": "Incidents cleared"}
