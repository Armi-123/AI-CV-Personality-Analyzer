# ============================================================
# PERSONAHIRE AI
# AI CV PERSONALITY ANALYZER
# ============================================================

"""
Main Streamlit application for PersonaHire AI.

Complete dynamic pipeline:

    Upload CV
        ↓
    PDF / DOCX Text Extraction
        ↓
    Text Preprocessing
        ↓
    Personality Prediction
        ↓
    Skill Extraction
        ↓
    Career Matching
        ↓
    Candidate Report
        ↓
    Download Analysis

Supported CV formats:
    - PDF
    - DOCX
"""

# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

import streamlit as st

from src.pdf_parser import extract_pdf_text
from src.docx_parser import extract_docx_text

from src.text_preprocessor import (
    preprocess_cv_text
)

from src.personality_predictor import (
    analyze_cv_personality
)

from src.skill_extractor import (
    analyze_cv_skills
)

from src.career_matcher import (
    analyze_career_fit
)

from src.report_generator import (
    generate_report,
    save_report_as_text
)


# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="PersonaHire AI",

    page_icon="🧠",

    layout="wide"

)

# ============================================================
# 3. APPLICATION TITLE
# ============================================================

st.title(
    "🧠 PersonaHire AI"
)

st.subheader(
    "AI-Powered CV Personality & Career Analyzer"
)

st.write(
    """
    Upload a candidate's CV to analyze personality traits,
    extract professional skills, and identify suitable
    career roles using machine learning.
    """
)

# ============================================================
# 4. SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "📋 Analysis Pipeline"
    )

    st.write(
        """
        1. 📄 CV Upload
        2. 📝 Text Extraction
        3. 🧹 Text Preprocessing
        4. 🧠 Personality Prediction
        5. 🛠️ Skill Extraction
        6. 💼 Career Matching
        7. 📊 Candidate Report
        """
    )

    st.divider()

    st.info(
        "Supported formats: PDF and DOCX"
    )

# ============================================================
# 5. CV UPLOAD
# ============================================================

uploaded_file = st.file_uploader(

    "Upload Candidate CV",

    type=[
        "pdf",
        "docx"
    ],

    help="Upload a PDF or DOCX resume."

)

# ============================================================
# 6. MAIN ANALYSIS
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # Display uploaded file
    # --------------------------------------------------------

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # --------------------------------------------------------
    # Candidate name
    # --------------------------------------------------------

    candidate_name = st.text_input(

        "Candidate Name",

        value="Candidate"

    )

    # --------------------------------------------------------
    # Start analysis button
    # --------------------------------------------------------

    analyze_button = st.button(

        "🚀 Analyze CV",

        type="primary",

        use_container_width=True

    )

    # ========================================================
    # RUN ANALYSIS
    # ========================================================

    if analyze_button:

        try:

            # ------------------------------------------------
            # 1. EXTRACT CV TEXT
            # ------------------------------------------------

            with st.spinner(
                "📄 Extracting CV text..."
            ):

                file_extension = (
                    uploaded_file.name
                    .lower()
                    .split(".")[-1]
                )

                # PDF extraction
                if file_extension == "pdf":

                    cv_text = extract_pdf_text(
                        uploaded_file
                    )

                # DOCX extraction
                elif file_extension == "docx":

                    cv_text = extract_docx_text(
                        uploaded_file
                    )

                else:

                    st.error(
                        "Unsupported file format."
                    )

                    st.stop()


            # ------------------------------------------------
            # Validate extracted text
            # ------------------------------------------------

            if not cv_text or not cv_text.strip():

                st.error(
                    "No readable text was found in the CV."
                )

                st.stop()


            # Store extracted text
            st.session_state[
                "cv_text"
            ] = cv_text


            # ------------------------------------------------
            # 2. PREPROCESS CV TEXT
            # ------------------------------------------------

            with st.spinner(
                "🧹 Preprocessing CV..."
            ):

                processed_text, statistics = (
                    preprocess_cv_text(
                        cv_text
                    )
                )


            st.session_state[
                "processed_text"
            ] = processed_text

            st.session_state[
                "statistics"
            ] = statistics


            # ------------------------------------------------
            # 3. PERSONALITY PREDICTION
            # ------------------------------------------------

            with st.spinner(
                "🧠 Predicting personality traits..."
            ):

                personality_result = (
                    analyze_cv_personality(
                        processed_text
                    )
                )


            st.session_state[
                "personality_result"
            ] = personality_result


            # ------------------------------------------------
            # 4. SKILL EXTRACTION
            # ------------------------------------------------

            with st.spinner(
                "🛠️ Extracting professional skills..."
            ):

                skill_result = (
                    analyze_cv_skills(
                        processed_text
                    )
                )


            st.session_state[
                "skill_result"
            ] = skill_result


            # ------------------------------------------------
            # 5. CAREER MATCHING
            # ------------------------------------------------

            with st.spinner(
                "💼 Matching suitable career roles..."
            ):

                career_result = (
                    analyze_career_fit(

                        skill_result,

                        personality_result,

                        top_n=5

                    )
                )


            st.session_state[
                "career_result"
            ] = career_result


            # ------------------------------------------------
            # 6. GENERATE COMPLETE REPORT
            # ------------------------------------------------

            with st.spinner(
                "📊 Generating candidate report..."
            ):

                report = generate_report(

                    personality_result,

                    skill_result,

                    candidate_name

                )


            st.session_state[
                "report"
            ] = report


            # ------------------------------------------------
            # Success message
            # ------------------------------------------------

            st.success(
                "✅ CV analysis completed successfully!"
            )


        except Exception as error:

            st.error(
                "❌ An error occurred during CV analysis."
            )

            st.exception(
                error
            )

# ============================================================
# 7. DISPLAY RESULTS
# ============================================================

if "personality_result" in st.session_state:

    personality_result = st.session_state[
        "personality_result"
    ]

    skill_result = st.session_state[
        "skill_result"
    ]

    career_result = st.session_state[
        "career_result"
    ]

    report = st.session_state[
        "report"
    ]

    # ========================================================
    # RESULTS HEADER
    # ========================================================

    st.divider()

    st.header(
        "📊 Candidate Analysis"
    )

    # ========================================================
    # 8. KEY METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Total Skills",

            skill_result[
                "total_skills"
            ]

        )

    with col2:

        st.metric(

            "Career Roles Analyzed",

            len(
                career_result[
                    "all_matches"
                ]
            )

        )

    with col3:

        st.metric(

            "Top Career Match",

            career_result[
                "top_careers"
            ][0]["role"]

            if career_result[
                "top_careers"
            ]

            else "N/A"

        )

    # ========================================================
    # 9. PERSONALITY ANALYSIS
    # ========================================================

    st.subheader(
        "🧠 Big Five Personality Analysis"
    )

    personality_data = []

    for trait, result in (
        personality_result[
            "traits"
        ].items()
    ):

        label = result[
            "label"
        ]

        confidence = result[
            "confidence"
        ]

        if label == 1:

            interpretation = (
                f"Higher predicted {trait}"
            )

        else:

            interpretation = (
                f"Lower predicted {trait}"
            )

        if confidence is not None:

            confidence_display = (
                f"{confidence * 100:.2f}%"
            )

        else:

            confidence_display = "N/A"

        personality_data.append({

            "Trait": trait,

            "Prediction": interpretation,

            "Confidence": confidence_display

        })


    st.dataframe(

        personality_data,

        use_container_width=True,

        hide_index=True

    )

    # ========================================================
    # 10. EXTRACTED SKILLS
    # ========================================================

    st.subheader(
        "🛠️ Extracted Skills"
    )

    all_skills = skill_result[
        "all_skills"
    ]

    if all_skills:

        # Display skills as columns
        skill_columns = st.columns(3)

        for index, skill in enumerate(
            all_skills
        ):

            with skill_columns[
                index % 3
            ]:

                st.write(
                    f"• {skill}"
                )

    else:

        st.warning(
            "No recognized skills were found."
        )

    # ========================================================
    # 11. SKILLS BY CATEGORY
    # ========================================================

    with st.expander(
        "View Skills by Category"
    ):

        for category, skills in (
            skill_result[
                "skills_by_category"
            ].items()
        ):

            if skills:

                st.write(
                    f"**{category}**"
                )

                st.write(
                    ", ".join(
                        skills
                    )
                )

    # ========================================================
    # 12. CAREER RECOMMENDATIONS
    # ========================================================

    st.subheader(
        "💼 Career Recommendations"
    )

    top_careers = career_result[
        "top_careers"
    ]


    for rank, career in enumerate(

        top_careers,

        start=1

    ):

        with st.container():

            st.markdown(
                f"### {rank}. {career['role']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Overall Match",

                    f"{career['overall_score']:.2f}%"

                )

            with col2:

                st.metric(

                    "Skill Match",

                    f"{career['skill_score']:.2f}%"

                )

            with col3:

                st.metric(

                    "Personality Match",

                    f"{career['personality_score']:.2f}%"

                )


            # Matching skills
            if career[
                "matched_skills"
            ]:

                st.write(
                    "**Matched Skills:**"
                )

                st.write(

                    ", ".join(
                        career[
                            "matched_skills"
                        ]
                    )

                )


            # Missing skills
            if career[
                "missing_skills"
            ]:

                st.write(
                    "**Skills to Improve:**"
                )

                st.write(

                    ", ".join(
                        career[
                            "missing_skills"
                        ]
                    )

                )

            st.divider()

    # ========================================================
    # 13. EXECUTIVE SUMMARY
    # ========================================================

    st.subheader(
        "📄 Executive Summary"
    )

    st.info(
        report[
            "executive_summary"
        ]
    )

    # ========================================================
    # 14. PROCESSED CV TEXT
    # ========================================================

    with st.expander(
        "View Extracted CV Text"
    ):

        st.text_area(

            "Processed CV Text",

            st.session_state[
                "processed_text"
            ],

            height=300

        )

    # ========================================================
    # 15. TEXT STATISTICS
    # ========================================================

    with st.expander(
        "View Text Statistics"
    ):

        st.json(
            st.session_state[
                "statistics"
            ]
        )

    # ========================================================
    # 16. GENERATE DOWNLOADABLE REPORT
    # ========================================================

    st.subheader(
        "📥 Download Candidate Report"
    )

    try:

        report_path = save_report_as_text(
            report
        )

        with open(

            report_path,

            "r",

            encoding="utf-8"

        ) as report_file:

            report_content = (
                report_file.read()
            )


        st.download_button(

            label="📥 Download Analysis Report",

            data=report_content,

            file_name="candidate_analysis_report.txt",

            mime="text/plain",

            use_container_width=True

        )

    except Exception as error:

        st.warning(
            f"Report download preparation failed: {error}"
        )

# ============================================================
# 17. INITIAL APPLICATION MESSAGE
# ============================================================

else:

    st.info(
        "👆 Upload a PDF or DOCX CV above to begin the analysis."
    )

# ============================================================
# 18. FOOTER
# ============================================================

st.divider()

st.caption(
    "PersonaHire AI | AI-Powered CV Personality & Career Analyzer"
)