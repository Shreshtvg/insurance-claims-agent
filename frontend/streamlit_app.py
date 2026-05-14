import streamlit as st
import requests
import json

st.set_page_config(
    page_title="LUMINA CLAIMS",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "data" not in st.session_state:
    st.session_state.data = None

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

# =========================
# HEADER
# =========================

st.markdown("""
# LUMINA CLAIMS
""")

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload FNOL Document",
    type=["pdf", "txt"]
)

# =========================
# CLEAR BUTTON
# =========================

if st.button("Clear Results"):

    st.session_state.data = None

    st.session_state.last_uploaded_file = None

    st.rerun()

# =========================
# PROCESS FILE
# =========================

if uploaded_file and (
    st.session_state.last_uploaded_file
    != uploaded_file.name
):

    with st.spinner(
        "Processing insurance claim..."
    ):

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }
        )

        data = response.json()

        st.session_state.data = data

        st.session_state.last_uploaded_file = (
            uploaded_file.name
        )

# =========================
# DISPLAY RESULTS
# =========================

if st.session_state.data:

    data = st.session_state.data

    extracted = data[
        "extractedFields"
    ]

    left, middle, right = st.columns(
        [1.1, 1.5, 1]
    )

    # =========================
    # LEFT PANEL
    # =========================

    with left:

        st.markdown("""
        ### SOURCE DOCUMENT
        """)

        st.write(
            st.session_state.last_uploaded_file
        )

        st.markdown("""
        ### STATEMENT OF LOSS
        """)

        st.write(
            extracted.get(
                "description",
                "Missing"
            )
        )

    # =========================
    # MIDDLE PANEL
    # =========================

    with middle:

        # POLICY INFO

        st.markdown("""
        ### POLICY INFORMATION
        """)

        st.write("policyNumber")
        st.markdown(
            f"**{extracted.get('policyNumber', 'Missing')}**"
        )

        st.write("policyholderName")
        st.markdown(
            f"**{extracted.get('policyholderName', 'Missing')}**"
        )

        st.write("effectiveDates")
        st.markdown(
            f"**{extracted.get('effectiveDates', 'Missing')}**"
        )

        # INCIDENT INFO

        st.markdown("""
        ### INCIDENT INFORMATION
        """)

        st.write("incidentDate")
        st.markdown(
            f"**{extracted.get('incidentDate', 'Missing')}**"
        )

        st.write("incidentTime")
        st.markdown(
            f"**{extracted.get('incidentTime', 'Missing')}**"
        )

        st.write("location")
        st.markdown(
            f"**{extracted.get('location', 'Missing')}**"
        )

        st.write("description")
        st.markdown(
            f"**{extracted.get('description', 'Missing')}**"
        )

        # INVOLVED PARTIES

        st.markdown("""
        ### INVOLVED PARTIES
        """)

        st.write("claimant")
        st.markdown(
            f"**{extracted.get('claimant', 'Missing')}**"
        )

        st.write("thirdParties")
        st.markdown(
            f"**{extracted.get('thirdParties', 'Missing')}**"
        )

        st.write("contactDetails")
        st.markdown(
            f"**{extracted.get('contactDetails', 'Missing')}**"
        )

        # ASSET DETAILS

        st.markdown("""
        ### ASSET DETAILS
        """)

        st.write("assetType")
        st.markdown(
            f"**{extracted.get('assetType', 'Missing')}**"
        )

        st.write("assetId")
        st.markdown(
            f"**{extracted.get('assetId', 'Missing')}**"
        )

        st.write("estimatedDamage")
        st.markdown(
            f"**{extracted.get('estimatedDamage', 'Missing')}**"
        )

        # OTHER FIELDS

        st.markdown("""
        ### OTHER MANDATORY FIELDS
        """)

        st.write("claimType")
        st.markdown(
            f"**{extracted.get('claimType', 'Missing')}**"
        )

        st.write("attachments")
        st.markdown(
            f"**{extracted.get('attachments', 'Missing')}**"
        )

        st.write("initialEstimate")
        st.markdown(
            f"**{extracted.get('initialEstimate', 'Missing')}**"
        )

    # =========================
    # RIGHT PANEL
    # =========================

    with right:

        st.markdown("""
        ### RECOMMENDED ROUTE
        """)

        route = data[
            "recommendedRoute"
        ]

        if route == "Fast-track":

            st.success(route)

        elif route == "Manual Review":

            st.warning(route)

        else:

            st.error(route)

        st.write(
            data["reasoning"]
        )

        st.markdown("""
        ### MISSING FIELDS
        """)

        if data["missingFields"]:

            for field in data[
                "missingFields"
            ]:

                st.error(field)

        else:

            st.success(
                "No missing fields"
            )

    # =========================
    # PIPELINE DEBUG
    # =========================

    st.divider()

    st.header(
        "AI Processing Pipeline"
    )

    with st.expander(
        "1. Parsed Document (OCR Output)"
    ):

        st.text(
            data["pipeline"][
                "parsedText"
            ]
        )

    with st.expander(
        "2. Raw LLM Response"
    ):

        st.code(
            data["pipeline"][
                "rawLLMOutput"
            ],
            language="json"
        )

    with st.expander(
        "3. Final Structured JSON"
    ):

        st.json(data["extractedFields"])

    # DOWNLOAD JSON

    st.download_button(
        label="Download JSON",
        data=json.dumps(
            data,
            indent=2
        ),
        file_name="claim_result.json",
        mime="application/json"
    )