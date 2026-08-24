# ============================================================
# SKILL EXTRACTOR
# AI CV Personality Analyzer
# ============================================================

"""
This module extracts technical and professional skills
from candidate CV/resume text.

Pipeline:

    CV Text
       ↓
    Text Preprocessing
       ↓
    Skill Detection
       ↓
    Extracted Skills
       ↓
    Category-wise Skill Summary

The extraction is dynamic:
the system analyzes the uploaded CV text rather than
using a fixed candidate profile.
"""


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# Import regular expressions for text matching
import re


# ============================================================
# 2. SKILL DATABASE
# ============================================================

"""
Common technical and professional skills.

The dictionary is organized by category so that the final
candidate report can show skills in a structured format.
"""

SKILL_DATABASE = {

    "Programming Languages": [

        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
        "R",
        "PHP",
        "Go",
        "Ruby",
        "Kotlin",
        "Swift"

    ],

    "Data Science & Machine Learning": [

        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Data Analysis",
        "Artificial Intelligence",
        "Natural Language Processing",
        "NLP",
        "Computer Vision",
        "Generative AI",
        "Generative Artificial Intelligence",
        "Large Language Models",
        "LLM",
        "Regression",
        "Classification",
        "Clustering",
        "Time Series",
        "Recommendation Systems",
        "Feature Engineering",
        "Predictive Modeling",
        "Statistical Modeling"

    ],

    "Python & Data Libraries": [

        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Scikit Learn",
        "SciPy",
        "Matplotlib",
        "Seaborn",
        "Plotly",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "OpenCV",
        "NLTK",
        "SpaCy"

    ],

    "Web Development": [

        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "React.js",
        "Node.js",
        "Express",
        "Express.js",
        "Flask",
        "Django",
        "FastAPI",
        "REST API",
        "REST APIs",
        "API Development"

    ],

    "Databases": [

        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite",
        "Oracle",
        "Redis",
        "Database Management"

    ],

    "Business Intelligence & Analytics": [

        "Power BI",
        "Tableau",
        "Excel",
        "Advanced Excel",
        "Power Query",
        "DAX",
        "Business Intelligence",
        "Data Visualization",
        "Dashboard Development",
        "Reporting",
        "MIS"

    ],

    "Cloud & DevOps": [

        "AWS",
        "Amazon Web Services",
        "Microsoft Azure",
        "Azure",
        "Google Cloud",
        "GCP",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "Jenkins",
        "GitHub Actions"

    ],

    "Tools & Technologies": [

        "Git",
        "GitHub",
        "GitLab",
        "Jupyter",
        "Jupyter Notebook",
        "Streamlit",
        "Gradio",
        "Postman",
        "VS Code",
        "Visual Studio Code",
        "Linux"

    ],

    "Generative AI & LLM Tools": [

        "LangChain",
        "LangGraph",
        "Hugging Face",
        "Transformers",
        "OpenAI",
        "Gemini",
        "Google Gemini",
        "RAG",
        "Retrieval Augmented Generation",
        "Prompt Engineering",
        "Vector Database",
        "FAISS",
        "ChromaDB"

    ],

    "Soft Skills": [

        "Communication",
        "Leadership",
        "Problem Solving",
        "Analytical Thinking",
        "Teamwork",
        "Time Management",
        "Critical Thinking",
        "Adaptability",
        "Creativity",
        "Collaboration"

    ]
}


# ============================================================
# 3. CREATE NORMALIZED SKILL LOOKUP
# ============================================================

def create_skill_lookup():
    """
    Create a normalized lookup dictionary.

    This makes matching case-insensitive while preserving
    the original skill name for the final output.

    Returns
    -------
    dict
        Normalized skill → original skill name.
    """

    skill_lookup = {}

    for category, skills in SKILL_DATABASE.items():

        for skill in skills:

            normalized_skill = skill.lower().strip()

            skill_lookup[
                normalized_skill
            ] = skill

    return skill_lookup


# ============================================================
# 4. NORMALIZE CV TEXT
# ============================================================

def normalize_cv_text(text):
    """
    Normalize CV text before skill extraction.

    Parameters
    ----------
    text : str
        Extracted CV text.

    Returns
    -------
    str
        Normalized CV text.
    """

    # Validate input
    if text is None:

        return ""

    # Convert input to string
    text = str(text)

    # Normalize multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# ============================================================
# 5. CHECK WHETHER SKILL EXISTS IN TEXT
# ============================================================

def skill_exists(
    text,
    skill
):
    """
    Check whether a particular skill exists in the CV.

    Word boundaries are used where possible to avoid
    incorrect matches.

    Parameters
    ----------
    text : str
        CV text.

    skill : str
        Skill to search for.

    Returns
    -------
    bool
        True if the skill is found.
    """

    # Escape special regex characters
    escaped_skill = re.escape(
        skill
    )

    # Create a case-insensitive pattern
    pattern = rf"(?<!\w){escaped_skill}(?!\w)"

    # Search the text
    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    return match is not None


# ============================================================
# 6. EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    """
    Extract skills dynamically from CV text.

    Parameters
    ----------
    text : str
        Candidate CV/resume text.

    Returns
    -------
    dict
        Category-wise extracted skills.
    """

    # Normalize CV text
    normalized_text = normalize_cv_text(
        text
    )

    # Validate text
    if not normalized_text:

        return {
            category: []
            for category in SKILL_DATABASE
        }

    # Store detected skills
    extracted_skills = {}

    # Search every category
    for category, skills in SKILL_DATABASE.items():

        category_skills = []

        # Check every skill
        for skill in skills:

            if skill_exists(
                normalized_text,
                skill
            ):

                category_skills.append(
                    skill
                )

        # Remove duplicates while preserving order
        category_skills = list(
            dict.fromkeys(
                category_skills
            )
        )

        extracted_skills[
            category
        ] = category_skills

    return extracted_skills


# ============================================================
# 7. GET FLAT SKILL LIST
# ============================================================

def get_flat_skill_list(
    extracted_skills
):
    """
    Convert category-wise skills into one list.

    Parameters
    ----------
    extracted_skills : dict
        Output from extract_skills().

    Returns
    -------
    list
        All detected skills.
    """

    all_skills = []

    for skills in extracted_skills.values():

        all_skills.extend(
            skills
        )

    # Remove duplicates
    all_skills = list(
        dict.fromkeys(
            all_skills
        )
    )

    return all_skills


# ============================================================
# 8. GET SKILL COUNTS
# ============================================================

def get_skill_counts(
    extracted_skills
):
    """
    Calculate skill counts by category.

    Parameters
    ----------
    extracted_skills : dict
        Category-wise extracted skills.

    Returns
    -------
    dict
        Category → number of detected skills.
    """

    category_counts = {}

    for category, skills in extracted_skills.items():

        category_counts[
            category
        ] = len(skills)

    return category_counts


# ============================================================
# 9. GET SKILL SUMMARY
# ============================================================

def get_skill_summary(
    extracted_skills
):
    """
    Generate a compact summary of extracted CV skills.

    Returns
    -------
    dict
        Complete skill summary.
    """

    # Get flat skill list
    all_skills = get_flat_skill_list(
        extracted_skills
    )

    # Get category counts
    category_counts = get_skill_counts(
        extracted_skills
    )

    # Count total skills
    total_skills = len(
        all_skills
    )

    return {

        "total_skills": total_skills,

        "all_skills": all_skills,

        "category_counts": category_counts,

        "skills_by_category": extracted_skills

    }


# ============================================================
# 10. COMPLETE SKILL EXTRACTION PIPELINE
# ============================================================

def analyze_cv_skills(
    text
):
    """
    Run the complete dynamic skill extraction pipeline.

    Parameters
    ----------
    text : str
        Candidate CV/resume text.

    Returns
    -------
    dict
        Complete skill analysis.
    """

    # Extract skills
    extracted_skills = extract_skills(
        text
    )

    # Generate summary
    summary = get_skill_summary(
        extracted_skills
    )

    return summary


# ============================================================
# 11. MODULE TEST
# ============================================================

if __name__ == "__main__":

    # Example CV text
    sample_cv = """
    Armi Sherathiya

    AI/ML Engineer and Data Scientist.

    Skills:
    Python, SQL, Pandas, NumPy, Scikit-learn,
    Machine Learning, Deep Learning, Power BI,
    Excel, Git, GitHub, Streamlit and Flask.

    Experience:
    Worked on data analysis, machine learning,
    dashboard development and AI projects.
    """

    # Run skill extraction
    result = analyze_cv_skills(
        sample_cv
    )

    # Display success message
    print(
        "Skill extractor module loaded successfully."
    )

    # Display total skills
    print(
        "\nTotal Skills:",
        result["total_skills"]
    )

    # Display all detected skills
    print(
        "\nDetected Skills:"
    )

    for skill in result["all_skills"]:

        print(
            f"- {skill}"
        )

    # Display category-wise results
    print(
        "\nSkills by Category:"
    )

    for category, skills in result[
        "skills_by_category"
    ].items():

        if skills:

            print(
                f"\n{category}:"
            )

            for skill in skills:

                print(
                    f"  - {skill}"
                )