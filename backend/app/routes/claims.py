import tempfile

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from app.services.mistral_ocr_service import (
    extract_text_using_mistral
)

from app.services.llm_service import (
    extract_claim_data
)

from app.services.validation_service import (
    validate_fields
)

from app.services.routing_service import (
    determine_route
)

PARSER_MODE = "mistral"

# OPTIONS:
# "mistral"
# "docling"

router = APIRouter()


@router.post("/analyze")
async def analyze_claim(
    file: UploadFile = File(...)
):

    contents = await file.read()

    parser_used = ""

    # =========================
    # TXT FILES
    # =========================

    if file.filename.endswith(".txt"):

        parsed_text = contents.decode(
            "utf-8"
        )

        parser_used = (
            "Direct Text Decode"
        )

    # =========================
    # PDF FILES
    # =========================

    else:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(contents)

            temp_path = tmp.name

        # =========================
        # MISTRAL OCR
        # =========================

        if PARSER_MODE == "mistral":

            parsed_text = (
                extract_text_using_mistral(
                    temp_path
                )
            )

            parser_used = (
                "Mistral OCR"
            )
        # =========================
        # FALLBACK
        # =========================

        else:

            parsed_text = (
                "Invalid parser mode"
            )

            parser_used = (
                "Unknown"
            )

    # =========================
    # LLM EXTRACTION
    # =========================

    extracted_fields = extract_claim_data(
        parsed_text
    )

    # =========================
    # VALIDATION
    # =========================

    missing_fields = validate_fields(
        extracted_fields
    )

    # =========================
    # ROUTING
    # =========================

    route, reasoning = determine_route(
        extracted_fields,
        missing_fields
    )

    # =========================
    # RESPONSE
    # =========================

    return {

        "pipeline": {

            "parserUsed": parser_used,

            "parsedText": parsed_text,

            "rawLLMOutput": extracted_fields.get(
                "_rawLLMOutput",
                ""
            )
        },

        "extractedFields": {

            k: v
            for k, v in extracted_fields.items()
            if not k.startswith("_")
        },

        "missingFields": missing_fields,

        "recommendedRoute": route,

        "reasoning": reasoning
    }