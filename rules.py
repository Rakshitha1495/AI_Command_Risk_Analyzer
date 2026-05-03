def analyze_command(command):
    cmd = command.lower().strip()
    base_cmd = cmd.split()[0] if cmd else ""

    high_risk_keywords = ["rm", "sudo", "format", "mkfs", "dd", "shutdown", "reboot"]
    if base_cmd in high_risk_keywords:
        return {
            "risk": "HIGH",
            "impact": "CRITICAL: Potential system-level change or permanent data loss detected.",
            "solution": "Halt execution. Verify target path and user permissions immediately."
        }

    med_risk_keywords = ["chmod", "chown", "mv", "cp", "apt", "pip", "install", "curl", "wget", "ssh", "git"]
    if base_cmd in med_risk_keywords:
        return {
            "risk": "MEDIUM",
            "impact": "MODIFICATION: Command alters file properties, network state, or installed software.",
            "solution": "Proceed with caution. Ensure source and destination/target are trusted."
        }

    low_risk_keywords = ["ls", "pwd", "whoami", "top", "df", "free", "cat", "grep", "history", "echo", "man", "cd", "clear"]
    if base_cmd in low_risk_keywords:
        return {
            "risk": "LOW",
            "impact": "This command appears safe and performs standard read-only operations.",
            "solution": "No action needed."
        }

    return {
        "risk": "LOW",
        "impact": "Standard operation detected.",
        "solution": "Standard execution path."
    }