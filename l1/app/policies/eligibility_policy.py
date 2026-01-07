# app/policies/eligibility_policy.py

def check_eligibility(matter_type: str, jurisdiction: str) -> dict:
    """
    Evaluates if the law firm can handle the case based on location and area of law.
    
    Args:
        matter_type: The area of law (e.g., 'property', 'criminal').
        jurisdiction: The city or state (e.g., 'Bangalore').
    """
    # Professional logic
    allowed_jurisdictions = ["bangalore", "mumbai", "delhi"]
    allowed_matters = ["property", "corporate", "family"]
    
    is_eligible = (
        jurisdiction.lower() in allowed_jurisdictions and 
        matter_type.lower() in allowed_matters
    )
    
    if is_eligible:
        return {"eligible": True, "message": "Lead meets firm criteria."}
    else:
        return {
            "eligible": False, 
            "reason": f"Firm does not practice {matter_type} in {jurisdiction}."
        }