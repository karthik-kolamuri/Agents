def check_eligibility(matter_type: str, jurisdiction: str) -> dict:
    """
    Evaluates if the firm can handle the case based on location and area of law.

    This is a lightweight eligibility policy used by the LegalIntakeMVP agent
    **before** booking any consultation.

    Args:
        matter_type: Area of law (e.g. "Property", "Criminal Offence").
        jurisdiction: City or region (e.g. "Hyderabad").

    Returns:
        dict with:
            - eligible: bool
            - message or reason: str
    """
    allowed_jurisdictions = ["bangalore", "mumbai", "delhi", "hyderabad"]
    allowed_matters = ["property", "corporate", "family", "criminal offence", "criminal"]

    is_eligible = (
        jurisdiction.lower() in allowed_jurisdictions
        and matter_type.lower() in allowed_matters
    )

    if is_eligible:
        return {
            "eligible": True,
            "message": "Lead meets firm criteria and can be accepted.",
        }

    return {
        "eligible": False,
        "reason": f"Firm does not practice {matter_type} in {jurisdiction}.",
    }

