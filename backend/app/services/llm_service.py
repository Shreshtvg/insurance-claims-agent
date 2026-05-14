import json
import re
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def clean_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:

        return match.group(0)

    return text


def empty_response():

    return {

        "policyNumber": None,

        "policyholderName": None,

        "effectiveDates": [],

        "incidentDate": None,

        "incidentTime": None,

        "location": None,

        "description": None,

        "claimant": None,

        "thirdParties": [],

        "contactDetails": None,

        "assetType": None,

        "assetId": None,

        "estimatedDamage": None,

        "claimType": None,

        "attachments": [],

        "initialEstimate": None,

        "isLikelyEmptyForm": True
    }


def extract_claim_data(text):

    prompt = f"""
You are an OCR information extraction system.

Extract ONLY exact values explicitly
present in the insurance FNOL document.

CRITICAL RULES:
- NEVER hallucinate.
- NEVER invent names.
- NEVER infer values.
- NEVER use placeholder examples.
- Ignore empty labels.
- If uncertain, return null.
- Copy values EXACTLY as written.
- Do not summarize.
- Return ONLY valid JSON.

The document may contain:
- tables
- checkboxes
- OCR noise
- multi-column layouts

JSON schema:

{{
    "policyNumber": null,
    "policyholderName": null,
    "effectiveDates": [],
    "incidentDate": null,
    "incidentTime": null,
    "location": null,
    "description": null,
    "claimant": null,
    "thirdParties": [],
    "contactDetails": null,
    "assetType": null,
    "assetId": null,
    "estimatedDamage": null,
    "claimType": null,
    "attachments": [],
    "initialEstimate": null
}}

Document:

{text}
"""

    completion = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    generated_text = (
        completion
        .choices[0]
        .message.content
    )

    cleaned = clean_json(
        generated_text
    )

    try:

        parsed = json.loads(
            cleaned
        )

        valid_values = 0

        for value in parsed.values():

            if value not in [
                None,
                "",
                [],
                {}
            ]:

                valid_values += 1

        parsed["isLikelyEmptyForm"] = (
            valid_values < 3
        )

        parsed["_rawLLMOutput"] = (
            generated_text
        )

        return parsed

    except Exception:

        response = empty_response()

        response["_rawLLMOutput"] = (
            generated_text
        )

        return response