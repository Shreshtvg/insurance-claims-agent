MANDATORY_FIELDS = [

    "policyNumber",

    "policyholderName",

    "incidentDate",

    "description",

    "claimant",

    "claimType"
]


def validate_fields(extracted_fields):

    missing_fields = []

    for field in MANDATORY_FIELDS:

        value = extracted_fields.get(
            field
        )

        if value in [
            None,
            "",
            [],
            {}
        ]:

            missing_fields.append(
                field
            )

    return missing_fields