# ============================================================
# REPORT GENERATOR
# AI CV Personality Analyzer
# ============================================================

"""
This module generates a structured candidate analysis report.

Input:
    1. Personality prediction results
    2. Extracted CV skills
    3. Optional candidate information

Output:
    Structured report data that can later be displayed in
    Streamlit and exported as PDF.

Pipeline:

    CV
     ↓
    Personality Predictor
     ↓
    Skill Extractor
     ↓
    Report Generator
     ↓
    Candidate Analysis Report
"""


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# Import os for file and directory handling
import os

# Import datetime for report generation timestamp
from datetime import datetime


# ============================================================
# 2. PROJECT PATH CONFIGURATION
# ============================================================

# Get the directory containing this file
CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Move from src/ to the project root
PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

# Define reports directory
REPORTS_DIR = os.path.join(
    PROJECT_ROOT,
    "reports"
)


# ============================================================
# 3. PERSONALITY TRAIT DESCRIPTIONS
# ============================================================

"""
Human-readable descriptions for the Big Five personality traits.

These descriptions are used only for report presentation.
They do not change the ML predictions.
"""

TRAIT_DESCRIPTIONS = {

    "Openness": (
        "Reflects openness to new ideas, experiences, "
        "creativity, curiosity, and adaptability."
    ),

    "Conscientiousness": (
        "Reflects organization, responsibility, "
        "discipline, planning, and goal orientation."
    ),

    "Extraversion": (
        "Reflects social engagement, communication, "
        "energy, assertiveness, and interaction."
    ),

    "Agreeableness": (
        "Reflects cooperation, empathy, consideration, "
        "trust, and interpersonal orientation."
    ),

    "Neuroticism": (
        "Reflects emotional sensitivity and tendency "
        "toward emotional reactions or stress."
    )
}


# ============================================================
# 4. TRAIT INTERPRETATION
# ============================================================

def interpret_trait(
    trait_name,
    label
):
    """
    Convert a binary personality prediction into a
    human-readable interpretation.

    Parameters
    ----------
    trait_name : str
        Big Five trait name.

    label : int
        Model prediction: 0 or 1.

    Returns
    -------
    str
        Human-readable interpretation.
    """

    # Prediction 1 represents the higher predicted class
    if int(label) == 1:

        return (
            f"Higher predicted {trait_name}"
        )

    # Prediction 0 represents the lower predicted class
    return (
        f"Lower predicted {trait_name}"
    )


# ============================================================
# 5. FORMAT CONFIDENCE
# ============================================================

def format_confidence(
    confidence
):
    """
    Convert a confidence value into a readable percentage.

    Parameters
    ----------
    confidence : float or None

    Returns
    -------
    str
        Formatted confidence.
    """

    # Confidence may not be available for every model
    if confidence is None:

        return "N/A"

    # Convert decimal confidence into percentage
    percentage = float(
        confidence
    ) * 100

    # Keep two decimal places
    return (
        f"{percentage:.2f}%"
    )


# ============================================================
# 6. BUILD PERSONALITY REPORT
# ============================================================

def build_personality_report(
    prediction_result
):
    """
    Convert personality predictor output into a structured
    report section.

    Parameters
    ----------
    prediction_result : dict
        Output from predict_personality() or
        analyze_cv_personality().

    Returns
    -------
    list
        Structured personality report.
    """

    # Store personality report items
    personality_report = []

    # Get prediction dictionary
    predictions = prediction_result.get(
        "predictions",
        {}
    )

    # Get confidence dictionary
    confidence_scores = prediction_result.get(
        "confidence",
        {}
    )

    # Process every Big Five trait
    for trait_name, description in TRAIT_DESCRIPTIONS.items():

        # Convert human-readable trait name back to prediction key
        trait_key = {

            "Openness": "O",
            "Conscientiousness": "C",
            "Extraversion": "E",
            "Agreeableness": "A",
            "Neuroticism": "N"

        }[trait_name]

        # Get prediction
        label = predictions.get(
            trait_key,
            None
        )

        # Get confidence
        confidence = confidence_scores.get(
            trait_key,
            None
        )

        # Create report item
        personality_report.append({

            "trait": trait_name,

            "prediction": label,

            "interpretation": (
                interpret_trait(
                    trait_name,
                    label
                )
                if label is not None
                else "Prediction unavailable"
            ),

            "confidence": confidence,

            "confidence_display": (
                format_confidence(
                    confidence
                )
                if confidence is not None
                else "N/A"
            ),

            "description": description

        })

    return personality_report


# ============================================================
# 7. BUILD SKILL REPORT
# ============================================================

def build_skill_report(
    skill_result
):
    """
    Convert skill extractor output into a structured
    report section.

    Parameters
    ----------
    skill_result : dict
        Output from analyze_cv_skills().

    Returns
    -------
    dict
        Structured skill report.
    """

    # Get all detected skills
    all_skills = skill_result.get(
        "all_skills",
        []
    )

    # Get category-wise skills
    skills_by_category = skill_result.get(
        "skills_by_category",
        {}
    )

    # Get total number of skills
    total_skills = skill_result.get(
        "total_skills",
        len(all_skills)
    )

    # Get category counts
    category_counts = skill_result.get(
        "category_counts",
        {}
    )

    return {

        "total_skills": total_skills,

        "all_skills": all_skills,

        "skills_by_category": skills_by_category,

        "category_counts": category_counts

    }


# ============================================================
# 8. CREATE EXECUTIVE SUMMARY
# ============================================================

def create_executive_summary(
    personality_report,
    skill_report
):
    """
    Create a concise candidate summary.

    This summary is generated from the model outputs and
    extracted skills. It does not invent candidate information.
    """

    # Count higher predicted traits
    higher_traits = [

        item["trait"]

        for item in personality_report

        if item["prediction"] == 1

    ]

    # Get total skill count
    total_skills = skill_report[
        "total_skills"
    ]

    # Create personality summary
    if higher_traits:

        personality_summary = (
            "Higher predicted traits: "
            + ", ".join(
                higher_traits
            )
            + "."
        )

    else:

        personality_summary = (
            "No higher predicted personality "
            "traits were identified."
        )

    # Create complete summary
    summary = (

        f"The CV analysis identified "
        f"{total_skills} skills. "

        f"{personality_summary}"

    )

    return summary


# ============================================================
# 9. GENERATE COMPLETE REPORT
# ============================================================

def generate_report(
    prediction_result,
    skill_result,
    candidate_name="Candidate"
):
    """
    Generate the complete candidate analysis report.

    Parameters
    ----------
    prediction_result : dict
        Output from personality prediction.

    skill_result : dict
        Output from skill extraction.

    candidate_name : str
        Candidate name for report presentation.

    Returns
    -------
    dict
        Complete structured candidate report.
    """

    # Create personality section
    personality_report = build_personality_report(
        prediction_result
    )

    # Create skills section
    skill_report = build_skill_report(
        skill_result
    )

    # Create executive summary
    executive_summary = create_executive_summary(
        personality_report,
        skill_report
    )

    # Generate current timestamp
    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Create complete report
    report = {

        "candidate_name": candidate_name,

        "generated_at": generated_at,

        "executive_summary": executive_summary,

        "personality_analysis": personality_report,

        "skills_analysis": skill_report

    }

    return report


# ============================================================
# 10. SAVE REPORT AS TEXT
# ============================================================

def save_report_as_text(
    report,
    filename=None
):
    """
    Save the structured report as a readable text file.

    Parameters
    ----------
    report : dict
        Generated candidate report.

    filename : str, optional
        Output file name.

    Returns
    -------
    str
        Path of saved report.
    """

    # Create reports directory if it does not exist
    os.makedirs(
        REPORTS_DIR,
        exist_ok=True
    )

    # Create default file name
    if filename is None:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"candidate_report_{timestamp}.txt"
        )

    # Create complete file path
    output_path = os.path.join(
        REPORTS_DIR,
        filename
    )

    # Open file for writing
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        # ----------------------------------------------------
        # Candidate information
        # ----------------------------------------------------

        file.write(
            "=" * 70
        )

        file.write(
            "\nAI CV PERSONALITY ANALYSIS REPORT\n"
        )

        file.write(
            "=" * 70
        )

        file.write(
            f"\n\nCandidate: "
            f"{report['candidate_name']}"
        )

        file.write(
            f"\nGenerated: "
            f"{report['generated_at']}"
        )

        # ----------------------------------------------------
        # Executive summary
        # ----------------------------------------------------

        file.write(
            "\n\n"
            + "-" * 70
        )

        file.write(
            "\nEXECUTIVE SUMMARY\n"
        )

        file.write(
            "-" * 70
        )

        file.write(
            f"\n{report['executive_summary']}\n"
        )

        # ----------------------------------------------------
        # Personality analysis
        # ----------------------------------------------------

        file.write(
            "\n\n"
            + "-" * 70
        )

        file.write(
            "\nPERSONALITY ANALYSIS\n"
        )

        file.write(
            "-" * 70
        )

        for item in report[
            "personality_analysis"
        ]:

            file.write(
                f"\n\nTrait: "
                f"{item['trait']}"
            )

            file.write(
                f"\nPrediction: "
                f"{item['interpretation']}"
            )

            file.write(
                f"\nConfidence: "
                f"{item['confidence_display']}"
            )

            file.write(
                f"\nDescription: "
                f"{item['description']}"
            )

        # ----------------------------------------------------
        # Skills analysis
        # ----------------------------------------------------

        file.write(
            "\n\n"
            + "-" * 70
        )

        file.write(
            "\nSKILLS ANALYSIS\n"
        )

        file.write(
            "-" * 70
        )

        file.write(
            f"\nTotal Skills: "
            f"{report['skills_analysis']['total_skills']}\n"
        )

        for category, skills in report[
            "skills_analysis"
        ][
            "skills_by_category"
        ].items():

            # Skip empty categories
            if not skills:

                continue

            file.write(
                f"\n\n{category}:\n"
            )

            for skill in skills:

                file.write(
                    f"  - {skill}\n"
                )

        # ----------------------------------------------------
        # Report footer
        # ----------------------------------------------------

        file.write(
            "\n\n"
            + "=" * 70
        )

        file.write(
            "\nGenerated by PersonaHire AI"
        )

        file.write(
            "\n"
            + "=" * 70
        )

    return output_path


# ============================================================
# 11. COMPLETE REPORT PIPELINE
# ============================================================

def analyze_candidate(
    prediction_result,
    skill_result,
    candidate_name="Candidate"
):
    """
    Create the complete candidate report and return it.

    This function will later be called by app.py.
    """

    # Generate report
    report = generate_report(

        prediction_result,

        skill_result,

        candidate_name

    )

    return report


# ============================================================
# 12. MODULE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Example personality prediction
    # --------------------------------------------------------

    sample_prediction = {

        "predictions": {

            "O": 1,
            "C": 1,
            "E": 0,
            "A": 1,
            "N": 0

        },

        "confidence": {

            "O": 0.82,
            "C": 0.76,
            "E": 0.71,
            "A": 0.79,
            "N": 0.68

        }

    }


    # --------------------------------------------------------
    # Example extracted skills
    # --------------------------------------------------------

    sample_skills = {

        "total_skills": 8,

        "all_skills": [

            "Python",
            "SQL",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Power BI",
            "Git",
            "Streamlit"

        ],

        "category_counts": {

            "Programming Languages": 1,

            "Data Science & Machine Learning": 1,

            "Python & Data Libraries": 2,

            "Databases": 1,

            "Business Intelligence & Analytics": 1,

            "Tools & Technologies": 2

        },

        "skills_by_category": {

            "Programming Languages": [
                "Python"
            ],

            "Data Science & Machine Learning": [
                "Machine Learning"
            ],

            "Python & Data Libraries": [
                "Pandas",
                "NumPy"
            ],

            "Databases": [
                "SQL"
            ],

            "Business Intelligence & Analytics": [
                "Power BI"
            ],

            "Tools & Technologies": [
                "Git",
                "Streamlit"
            ]

        }

    }


    # --------------------------------------------------------
    # Generate report
    # --------------------------------------------------------

    report = analyze_candidate(

        sample_prediction,

        sample_skills,

        candidate_name="Sample Candidate"

    )


    # --------------------------------------------------------
    # Display report
    # --------------------------------------------------------

    print(
        "Report generator module loaded successfully."
    )

    print(
        "\nCandidate:",
        report["candidate_name"]
    )

    print(
        "\nGenerated:",
        report["generated_at"]
    )

    print(
        "\nExecutive Summary:"
    )

    print(
        report["executive_summary"]
    )

    print(
        "\nPersonality Analysis:"
    )

    for item in report[
        "personality_analysis"
    ]:

        print(
            f"- {item['trait']}: "
            f"{item['interpretation']} "
            f"({item['confidence_display']})"
        )

    print(
        "\nSkills:"
    )

    for skill in report[
        "skills_analysis"
    ][
        "all_skills"
    ]:

        print(
            f"- {skill}"
        )

    # --------------------------------------------------------
    # Save text report
    # --------------------------------------------------------

    output_file = save_report_as_text(
        report
    )

    print(
        "\nReport saved successfully:"
    )

    print(
        output_file
    )