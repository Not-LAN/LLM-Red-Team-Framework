OWASP_DESCRIPTIONS = {
    "OWASP-LLM01": "Prompt Injection - Manipulating the model’s behavior through crafted inputs.",
    "OWASP-LLM02": "Data Leakage - Causing the model to reveal sensitive or synthetic information.",
    "OWASP-LLM03": "Training Data Poisoning - Model influenced by malicious training data.",
    "OWASP-LLM04": "Model Denial of Service - Causing performance degradation or instability.",
    "OWASP-LLM05": "Supply Chain Vulnerabilities - Insecure dependencies in model pipelines.",
    "OWASP-LLM06": "Sensitive Information Disclosure - Leaking PII or internal logic.",
    "OWASP-LLM07": "Insecure Plugins / Tools - Unsafe execution of model-integrated functions.",
    "OWASP-LLM08": "Excessive Agency - Dangerous autonomous behavior.",
    "OWASP-LLM09": "Overreliance - Blind trust in incorrect or hallucinated output.",
    "OWASP-LLM10": "Model Theft - Reconstructing proprietary model behavior via output."
}

ATLAS_TACTICS = {
    "ATLAS-TA0001": "Reconnaissance – Gathering information to plan future attacks.",
    "ATLAS-TA0002": "Resource Development – Establishing resources to support operations.",
    "ATLAS-TA0003": "Initial Access – Gaining entry into AI systems.",
    "ATLAS-TA0004": "Execution – Running malicious code or commands.",
    "ATLAS-TA0005": "Persistence – Maintaining access to AI systems.",
    "ATLAS-TA0006": "Privilege Escalation – Gaining higher-level permissions.",
    "ATLAS-TA0007": "Defense Evasion – Avoiding detection and security measures.",
    "ATLAS-TA0008": "Credential Access – Stealing credentials like usernames and passwords.",
    "ATLAS-TA0009": "Discovery – Identifying system information and internal configurations.",
    "ATLAS-TA0010": "Lateral Movement – Moving through systems within a network.",
    "ATLAS-TA0011": "Collection – Gathering data of interest to the adversary.",
    "ATLAS-TA0012": "Exfiltration – Transmitting stolen data out of the network.",
    "ATLAS-TA0013": "Impact – Manipulating, interrupting, or destroying systems and data.",
    "ATLAS-TA0014": "Command and Control – Communicating with compromised systems."
}


def get_owasp_description(tag: str) -> str:
    return OWASP_DESCRIPTIONS.get(tag, "No description available for this OWASP tag.")


def get_atlas_tactic_name(tactic_id: str) -> str:
    if not tactic_id.startswith("ATLAS-"):
        tactic_id = f"ATLAS-{tactic_id}"
    return ATLAS_TACTICS.get(tactic_id, "Unknown MITRE ATLAS tactic.")
