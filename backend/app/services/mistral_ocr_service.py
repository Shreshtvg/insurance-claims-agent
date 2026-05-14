import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "MISTRAL_API_KEY"
)


def extract_text_using_mistral(
    file_path
):

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    # =========================
    # UPLOAD FILE
    # =========================

    with open(file_path, "rb") as f:

        files = {
            "file": (
                "document.pdf",
                f,
                "application/pdf"
            )
        }

        data = {
            "purpose": "ocr"
        }

        upload_response = requests.post(
            "https://api.mistral.ai/v1/files",
            headers=headers,
            files=files,
            data=data
        )

    upload_json = (
        upload_response.json()
    )

    file_id = upload_json["id"]

    # =========================
    # GET SIGNED URL
    # =========================

    signed_url_response = requests.get(
        f"https://api.mistral.ai/v1/files/{file_id}/url",
        headers=headers
    )

    signed_url = (
        signed_url_response
        .json()["url"]
    )

    # =========================
    # OCR PROCESS
    # =========================

    ocr_payload = {

        "model": "mistral-ocr-latest",

        "document": {

            "type": "document_url",

            "document_url": signed_url
        }
    }

    ocr_response = requests.post(
        "https://api.mistral.ai/v1/ocr",
        headers={
            **headers,
            "Content-Type": "application/json"
        },
        json=ocr_payload
    )

    ocr_json = ocr_response.json()

    extracted_text = ""

    for page in ocr_json["pages"]:

        extracted_text += (
            page["markdown"] + "\n"
        )

    return extracted_text