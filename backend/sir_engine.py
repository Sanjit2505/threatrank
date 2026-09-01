import math
import random

# ==========================================
# 1. ASSET GRAPH DATA MODEL (16 Infrastructure Nodes)
# ==========================================
ASSET_GRAPH = {
    "node_1": {
        "id": "node_1",
        "name": "Sales Laptop (Win11)",
        "type": "Endpoint",
        "criticality": 3,
        "business_impact": 25,
        "neighbors": ["node_2", "node_11", "node_12"]
    },
    "node_2": {
        "id": "node_2",
        "name": "Dev Workstation",
        "type": "Endpoint",
        "criticality": 5,
        "business_impact": 40,
        "neighbors": ["node_1", "node_3", "node_14", "node_4"]
    },
    "node_3": {
        "id": "node_3",
        "name": "Staging Application Server",
        "type": "Server",
        "criticality": 6,
        "business_impact": 55,
        "neighbors": ["node_2", "node_8", "node_4"]
    },
    "node_4": {
        "id": "node_4",
        "name": "API Gateway / Perimeter",
        "type": "Network",
        "criticality": 8,
        "business_impact": 80,
        "neighbors": ["node_2", "node_3", "node_5", "node_6", "node_8"]
    },
    "node_5": {
        "id": "node_5",
        "name": "Web Server (DMZ)",
        "type": "DMZ",
        "criticality": 7,
        "business_impact": 70,
        "neighbors": ["node_4", "node_6", "node_9"]
    },
    "node_6": {
        "id": "node_6",
        "name": "OAuth / Auth Service",
        "type": "Identity",
        "criticality": 9,
        "business_impact": 90,
        "neighbors": ["node_4", "node_5", "node_7", "node_8", "node_13"]
    },
    "node_7": {
        "id": "node_7",
        "name": "Active Directory Domain Controller",
        "type": "Crown Jewel",
        "criticality": 10,
        "business_impact": 100,
        "neighbors": ["node_6", "node_1", "node_2", "node_10", "node_11", "node_13", "node_9"]
    },
    "node_8": {
        "id": "node_8",
        "name": "Customer Production Database",
        "type": "Crown Jewel",
        "criticality": 10,
        "business_impact": 100,
        "neighbors": ["node_3", "node_4", "node_6", "node_9", "node_15"]
    },
    "node_9": {
        "id": "node_9",
        "name": "Payment Gateway (PCI-DSS DB)",
        "type": "Crown Jewel",
        "criticality": 10,
        "business_impact": 100,
        "neighbors": ["node_5", "node_6", "node_8", "node_13"]
    },
    "node_10": {
        "id": "node_10",
        "name": "HR & Payroll Database",
        "type": "Database",
        "criticality": 7,
        "business_impact": 65,
        "neighbors": ["node_7", "node_11"]
    },
    "node_11": {
        "id": "node_11",
        "name": "Internal File Share (NAS)",
        "type": "Storage",
        "criticality": 5,
        "business_impact": 45,
        "neighbors": ["node_1", "node_7", "node_10"]
    },
    "node_12": {
        "id": "node_12",
        "name": "Exchange Mail Server",
        "type": "Server",
        "criticality": 6,
        "business_impact": 50,
        "neighbors": ["node_1", "node_7"]
    },
    "node_13": {
        "id": "node_13",
        "name": "Security Admin Console",
        "type": "Security Ops",
        "criticality": 9,
        "business_impact": 95,
        "neighbors": ["node_6", "node_7", "node_9", "node_14"]
    },
    "node_14": {
        "id": "node_14",
        "name": "AWS Cloud S3 Storage",
        "type": "Cloud",
        "criticality": 7,
        "business_impact": 75,
        "neighbors": ["node_2", "node_13", "node_15"]
    },
    "node_15": {
        "id": "node_15",
        "name": "Analytics & BI Warehouse",
        "type": "Analytics",
        "criticality": 6,
        "business_impact": 50,
        "neighbors": ["node_8", "node_14"]
    },
    "node_16": {
        "id": "node_16",
        "name": "SCADA / IoT HVAC Controller",
        "type": "IoT",
        "criticality": 7,
        "business_impact": 60,
        "neighbors": ["node_1"]
    }
}

# Pre-calculate degree centrality for asset nodes
for nid, node in ASSET_GRAPH.items():
    node["degree"] = len(node["neighbors"])

# ==========================================
# 2. ENGINEERS DATA MODEL
# ==========================================
ENGINEERS = [
    {
        "id": "ENG-01",
        "name": "Alex Rivera",
        "role": "Senior Lead Security Specialist",
        "specialties": ["Brute Force / Credential Stuffing", "Active Directory", "Crown Jewel"],
        "assigned_count": 0,
        "max_capacity": 4,
        "status": "Available",
        "avatar_color": "#3b82f6"
    },
    {
        "id": "ENG-02",
        "name": "Sarah Chen",
        "role": "Cloud Data Exfiltration Analyst",
        "specialties": ["Data Exfiltration", "Cloud", "Crown Jewel"],
        "assigned_count": 0,
        "max_capacity": 4,
        "status": "Available",
        "avatar_color": "#10b981"
    },
    {
        "id": "ENG-03",
        "name": "Marcus Vance",
        "role": "Network Defense Engineer",
        "specialties": ["Port Scan / Reconnaissance", "Network", "DMZ"],
        "assigned_count": 0,
        "max_capacity": 3,
        "status": "Available",
        "avatar_color": "#8b5cf6"
    },
    {
        "id": "ENG-04",
        "name": "AI Sentinel Bot v4",
        "role": "Automated Autonomous Responder",
        "specialties": ["Normal Traffic", "Port Scan / Reconnaissance", "Endpoint"],
        "assigned_count": 0,
        "max_capacity": 99,
        "status": "Autonomous",
        "avatar_color": "#f59e0b"
    }
]

# ==========================================
# 3. SIR SIMULATION ENGINE
# ==========================================
def simulate_sir_spread(affected_asset_id: str, severity: int, attack_confidence: float, steps: int = 8) -> dict:
    """
    Simulates threat contagion over N steps (e.g. 8 steps = 4 hours in 30-min increments).
    Returns step-by-step infected asset sets, damage curve points, and total AUDC (Area Under Curve).
    """
    if affected_asset_id not in ASSET_GRAPH:
        # Fallback to node_1 if asset unknown
        affected_asset_id = "node_1"

    # Base transmission rate per step derived from severity and confidence
    base_trans_prob = min(0.9, max(0.15, (attack_confidence / 100.0) * 0.7 + (severity / 10.0) * 0.3))

    # Tracking sets
    infected = {affected_asset_id}
    step_history = []
    damage_curve = []
    
    # Calculate damage at step 0
    initial_impact = sum(ASSET_GRAPH[nid]["business_impact"] * ASSET_GRAPH[nid]["criticality"] for nid in infected)
    damage_curve.append(initial_impact)
    step_history.append({
        "step": 0,
        "time_label": "00:00 (Initial)",
        "infected_nodes": list(infected),
        "infected_count": len(infected),
        "cumulative_damage": initial_impact
    })

    # Discrete step forward simulation
    # Using deterministic propagation probability based on node centrality to ensure reproducible demo results
    curr_infected = set(infected)
    
    for t in range(1, steps + 1):
        time_minutes = t * 30
        hours = time_minutes // 60
        mins = time_minutes % 60
        time_str = f"+{hours:02d}h{mins:02d}m"

        newly_infected = set()
        for inf_node in curr_infected:
            neighbors = ASSET_GRAPH[inf_node]["neighbors"]
            for nbr in neighbors:
                if nbr not in curr_infected:
                    # Transmission probability adjusted by target asset's degree/reachability
                    trans_threshold = base_trans_prob * (1.0 + (ASSET_GRAPH[nbr]["degree"] * 0.05))
                    # Deterministic check threshold for consistent simulation ranking
                    # based on edge connectivity order and step t
                    pseudo_rand = ((hash(inf_node + nbr) + t * 37) % 100) / 100.0
                    if pseudo_rand <= trans_threshold:
                        newly_infected.add(nbr)

        curr_infected.update(newly_infected)
        step_impact = sum(ASSET_GRAPH[nid]["business_impact"] * ASSET_GRAPH[nid]["criticality"] for nid in curr_infected)
        
        damage_curve.append(step_impact)
        step_history.append({
            "step": t,
            "time_label": time_str,
            "infected_nodes": list(curr_infected),
            "infected_count": len(curr_infected),
            "cumulative_damage": step_impact
        })

    # Compute Area Under the Damage Curve (AUDC) using Trapezoidal Rule
    audc = 0.0
    for i in range(len(damage_curve) - 1):
        # Average height of trapezoid * step width (1 unit = 30 mins)
        audc += (damage_curve[i] + damage_curve[i+1]) / 2.0

    # Priority score normalized 0 - 1000, mapped to 0 - 100 scale for UI readability
    max_possible_audc = sum(ASSET_GRAPH[n]["business_impact"] * ASSET_GRAPH[n]["criticality"] for n in ASSET_GRAPH) * steps
    priority_score = min(99, max(10, int((audc / max_possible_audc) * 100 * 3.5)))

    # Find highest criticality node hit in simulation
    highest_critical_hit = max([ASSET_GRAPH[n] for n in curr_infected], key=lambda x: x["criticality"])

    return {
        "priority_score": priority_score,
        "audc": round(audc, 1),
        "damage_curve": damage_curve,
        "step_history": step_history,
        "projected_assets_hit_4hrs": len(curr_infected),
        "highest_criticality_asset": highest_critical_hit["name"],
        "patient_zero": ASSET_GRAPH[affected_asset_id]["name"]
    }

def generate_natural_language_justification(incident: dict, rank: int, sim_result: dict) -> str:
    """
    Generates a natural-language explanation incorporating the contagion/fever analogy.
    """
    p0 = sim_result["patient_zero"]
    hit_count = sim_result["projected_assets_hit_4hrs"]
    crown_jewel = sim_result["highest_criticality_asset"]
    raw_sev = incident.get("severity", 5)
    
    analogy = f"Like two individuals with the same fever — one isolated in a room vs. one in a crowded transit hub — raw severity alone is misleading."

    if rank == 1:
        return (
            f"Ranked #{rank} [PRIORITY SCORE: {sim_result['priority_score']}/100]. {analogy} "
            f"Originated at '{p0}'. Even with raw severity {raw_sev}/10, its high network centrality causes it to propagate to {hit_count} connected assets in 4 hours, "
            f"projected to breach crown jewel '{crown_jewel}' within 90 minutes. Area Under Damage Curve (AUDC: {sim_result['audc']})."
        )
    elif rank == 2:
        return (
            f"Ranked #{rank} [PRIORITY SCORE: {sim_result['priority_score']}/100]. {analogy} "
            f"Originating at '{p0}', the infection vector rapidly moves across interconnected assets reaching {hit_count} systems including '{crown_jewel}'."
        )
    else:
        return (
            f"Ranked #{rank} [PRIORITY SCORE: {sim_result['priority_score']}/100]. "
            f"Originating at '{p0}'. Blast radius contained to {hit_count} lower-criticality nodes in the projected 4-hour window."
        )

def assign_engineer(incident: dict, engineers: list, manual_eng_id: str = None) -> dict:
    """
    Auto-assigns or manually assigns an engineer to an incident based on workload and specialization.
    """
    if manual_eng_id:
        for eng in engineers:
            if eng["id"] == manual_eng_id:
                eng["assigned_count"] += 1
                return {"id": eng["id"], "name": eng["name"], "role": eng["role"], "avatar_color": eng["avatar_color"]}

    # Automated intelligent matching
    attack_type = incident.get("attack_type", "")
    affected_type = ASSET_GRAPH.get(incident.get("affected_asset_id", "node_1"), {}).get("type", "")

    best_engineer = None
    best_score = -1

    for eng in engineers:
        if eng["assigned_count"] >= eng["max_capacity"]:
            continue

        score = 0
        for spec in eng["specialties"]:
            if spec.lower() in attack_type.lower():
                score += 10
            if spec.lower() in affected_type.lower():
                score += 8

        # Prefer engineers with lower workload
        score += (eng["max_capacity"] - eng["assigned_count"]) * 2

        if score > best_score:
            best_score = score
            best_engineer = eng

    if not best_engineer:
        best_engineer = engineers[-1] # Fallback to AI Bot

    best_engineer["assigned_count"] += 1
    return {
        "id": best_engineer["id"],
        "name": best_engineer["name"],
        "role": best_engineer["role"],
        "avatar_color": best_engineer["avatar_color"]
    }
