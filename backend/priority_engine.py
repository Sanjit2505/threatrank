def calculate_priority(attack_type, confidence_pct, severity, asset_criticality, business_impact, affected_users):
    """
    Calculates a dynamic priority score from 0-100 based on AI confidence and organizational impact metrics.
    """
    # Normalize inputs somewhat
    sev_score = min(severity, 10) * 2  # up to 20
    asset_score = min(asset_criticality, 10) * 2 # up to 20
    biz_score = min(business_impact, 10) * 2 # up to 20
    users_score = min(affected_users / 5, 10) # 50 users -> max 10
    
    # Confidence weight (up to 30)
    conf_score = (confidence_pct / 100.0) * 30
    
    total_score = sev_score + asset_score + biz_score + users_score + conf_score
    
    # Cap at 100
    return min(int(total_score), 100)

def sort_incidents(incidents: list):
    """
    Sorts a list of incident dictionaries in-place by priority_score descending (top score first).
    """
    incidents.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
