RECOMMENDED_ACTIONS = {
    "normal": [
        "No action required.",
        "Continue standard monitoring."
    ],
    "brute_force": [
        "Temporarily block the suspicious source.",
        "Investigate affected accounts.",
        "Review authentication logs.",
        "Enable or verify MFA.",
        "Monitor for further attempts."
    ],
    "generic_attack": [
        "Investigate the source IP.",
        "Review IPS/IDS logs for specific signatures.",
        "Block the source if malicious."
    ],
    "exploit": [
        "Identify the targeted vulnerability.",
        "Patch or apply mitigation to the affected asset.",
        "Review web application firewall (WAF) logs.",
        "Isolate asset if successfully exploited."
    ],
    "fuzzing": [
        "Block the source IP address.",
        "Verify application stability and resource consumption.",
        "Tune WAF rules to drop fuzzing payloads."
    ],
    "dos": [
        "Enable DDoS protection/rate limiting.",
        "Null-route the malicious traffic upstream.",
        "Ensure critical services are highly available."
    ],
    "reconnaissance": [
        "Monitor the source for subsequent attack phases.",
        "Ensure external attack surface is minimized.",
        "Block the IP if port scanning is aggressive."
    ],
    "intrusion": [
        "Immediately isolate the compromised system.",
        "Initiate incident response procedures.",
        "Preserve memory and disk artifacts.",
        "Identify and rotate potentially compromised credentials."
    ],
    "analysis": [
        "Review the nature of the analysis/scanning.",
        "Block the source if unauthorized."
    ],
    "backdoor": [
        "Isolate the affected system immediately.",
        "Identify the command and control (C2) channel.",
        "Block the C2 IP/domain at the firewall.",
        "Perform a full forensic analysis."
    ],
    "shellcode": [
        "Investigate the targeted service for buffer overflow vulnerabilities.",
        "Apply latest security patches.",
        "Block the source IP."
    ],
    "worm": [
        "Isolate affected subnet immediately.",
        "Deploy anti-malware signatures.",
        "Identify the initial infection vector.",
        "Patch vulnerable services across the network."
    ],
    "data_exfiltration": [
        "Escalate immediately.",
        "Contain suspicious data access.",
        "Preserve logs and evidence.",
        "Identify affected systems and data.",
        "Follow the organization's incident-response process."
    ]
}

def get_recommended_action(attack_type):
    """
    Returns a list of recommended actions for a given attack type.
    """
    return RECOMMENDED_ACTIONS.get(attack_type, [
        "Investigate the alert.",
        "Review system logs.",
        "Determine if the activity is authorized."
    ])
