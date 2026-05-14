def determine_route(
    extracted_fields,
    missing_fields
):

    description = str(
        extracted_fields.get(
            "description",
            ""
        )
    ).lower()

    claim_type = str(
        extracted_fields.get(
            "claimType",
            ""
        )
    ).lower()

    estimated_damage = str(
        extracted_fields.get(
            "estimatedDamage",
            ""
        )
    )

    # MISSING FIELDS
    if missing_fields:

        return (
            "Manual Review",
            "Mandatory fields are missing."
        )

    # FRAUD WORDS
    fraud_keywords = [

        "fraud",

        "staged",

        "inconsistent"
    ]

    if any(
        word in description
        for word in fraud_keywords
    ):

        return (
            "Investigation Flag",
            "Potential fraud indicators detected."
        )

    # INJURY CLAIM
    if claim_type == "injury":

        return (
            "Specialist Queue",
            "Injury-related claim detected."
        )

    # FAST TRACK
    try:

        damage_value = int(

            estimated_damage
            .replace("$", "")
            .replace(",", "")
        )

        if damage_value < 25000:

            return (
                "Fast-track",
                "Low estimated damage."
            )

    except Exception:

        pass

    return (
        "Manual Review",
        "Unable to confidently auto-route."
    )