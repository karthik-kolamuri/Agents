SUPPORTED_JURISDICTIONS = {"bangalore", "chennai", "hyderabad"}

def check_eligibility(lead: dict) -> dict:
    if lead["jurisdiction"].lower() not in SUPPORTED_JURISDICTIONS:
        return {"eligible": False, "reason": "Unsupported jurisdiction"}
    return {"eligible": True}
