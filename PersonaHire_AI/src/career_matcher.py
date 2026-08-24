# ============================================================
# CAREER MATCHER
# PersonaHire AI
# ============================================================

"""
This module matches a candidate CV with suitable career roles.

Input:
    1. Extracted skills
    2. Big Five personality predictions

Output:
    1. Career match score
    2. Matching skills
    3. Missing skills
    4. Personality alignment
    5. Ranked career recommendations

The matching is dynamic and works with the candidate's
actual extracted CV information.
"""


# ============================================================
# 1. CAREER ROLE DATABASE
# ============================================================

CAREER_ROLES = {

    "Data Scientist": {

        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Data Science",
            "Data Analysis",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Statistics",
            "Data Visualization"
        ],

        "personality": {
            "O": 1,
            "C": 1,
            "E": 0,
            "A": 0,
            "N": 0
        }

    },

    "Data Analyst": {

        "skills": [
            "Python",
            "SQL",
            "Data Analysis",
            "Pandas",
            "NumPy",
            "Excel",
            "Power BI",
            "Tableau",
            "Data Visualization",
            "Statistics"
        ],

        "personality": {
            "O": 1,
            "C": 1,
            "E": 0,
            "A": 1,
            "N": 0
        }

    },

    "Machine Learning Engineer": {

        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Scikit-learn",
            "TensorFlow",
            "PyTorch",
            "Git",
            "Docker",
            "SQL",
            "API Development"
        ],

        "personality": {
            "O": 1,
            "C": 1,
            "E": 0,
            "A": 0,
            "N": 0
        }

    },

    "AI Engineer": {

        "skills": [
            "Python",
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning",
            "Natural Language Processing",
            "Generative AI",
            "LLM",
            "TensorFlow",
            "PyTorch",
            "Git"
        ],

        "personality": {
            "O": 1,
            "C": 1,
            "E": 0,
            "A": 0,
            "N": 0
        }

    },

    "Power BI Analyst": {

        "skills": [
            "Power BI",
            "Excel",
            "SQL",
            "DAX",
            "Power Query",
            "Data Analysis",
            "Data Visualization",
            "Dashboard Development",
            "Reporting",
            "MIS"
        ],

        "personality": {
            "O": 0,
            "C": 1,
            "E": 1,
            "A": 1,
            "N": 0
        }

    },

    "Python Developer": {

        "skills": [
            "Python",
            "Flask",
            "Django",
            "FastAPI",
            "REST API",
            "SQL",
            "Git",
            "GitHub",
            "Postman",
            "API Development"
        ],

        "personality": {
            "O": 1,
            "C": 1,
            "E": 0,
            "A": 0,
            "N": 0
        }

    },

    "Business Analyst": {

        "skills": [
            "SQL",
            "Excel",
            "Power BI",
            "Data Analysis",
            "Reporting",
            "Business Intelligence",
            "Communication",
            "Problem Solving",
            "Analytical Thinking",
            "Dashboard Development"
        ],

        "personality": {
            "O": 0,
            "C": 1,
            "E": 1,
            "A": 1,
            "N": 0
        }

    },

    "Full Stack Developer": {

        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express.js",
            "MongoDB",
            "SQL",
            "Git",
            "REST API"
        ],

        "personality": {
            "O": 1,
            "C": 1,
            "E": 1,
            "A": 0,
            "N": 0
        }

    }

}


# ============================================================
# 2. PERSONALITY TRAIT NAMES
# ============================================================

TRAIT_NAMES = {

    "O": "Openness",

    "C": "Conscientiousness",

    "E": "Extraversion",

    "A": "Agreeableness",

    "N": "Neuroticism"

}


# ============================================================
# 3. NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):
    """
    Normalize a skill name for comparison.
    """

    return (
        str(skill)
        .strip()
        .lower()
    )


# ============================================================
# 4. PREPARE CANDIDATE SKILLS
# ============================================================

def prepare_candidate_skills(
    skill_result
):
    """
    Extract candidate skills from the output of
    skill_extractor.py.

    Parameters
    ----------
    skill_result : dict
        Output from analyze_cv_skills().

    Returns
    -------
    set
        Normalized candidate skills.
    """

    # Get flat skill list
    skills = skill_result.get(
        "all_skills",
        []
    )

    # Normalize every skill
    normalized_skills = {

        normalize_skill(skill)

        for skill in skills

    }

    return normalized_skills


# ============================================================
# 5. CALCULATE SKILL MATCH
# ============================================================

def calculate_skill_match(
    candidate_skills,
    required_skills
):
    """
    Calculate career-role skill matching.

    Returns:
        score
        matched skills
        missing skills
    """

    # Normalize required skills
    normalized_required = {

        normalize_skill(skill)

        for skill in required_skills

    }

    # Find matching skills
    matched_skills = (

        candidate_skills
        & normalized_required

    )

    # Find missing skills
    missing_skills = (

        normalized_required
        - candidate_skills

    )

    # Calculate percentage
    if len(normalized_required) == 0:

        skill_score = 0.0

    else:

        skill_score = (

            len(matched_skills)
            / len(normalized_required)

        ) * 100

    return {

        "score": round(
            skill_score,
            2
        ),

        "matched_skills": sorted(
            matched_skills
        ),

        "missing_skills": sorted(
            missing_skills
        )

    }


# ============================================================
# 6. CALCULATE PERSONALITY MATCH
# ============================================================

def calculate_personality_match(
    predictions,
    required_personality
):
    """
    Compare candidate personality predictions with the
    personality profile expected for a career role.

    Parameters
    ----------
    predictions : dict
        O/C/E/A/N predictions.

    required_personality : dict
        Expected personality profile.

    Returns
    -------
    dict
        Personality score and matching traits.
    """

    # Store matching traits
    matching_traits = []

    # Store mismatching traits
    mismatching_traits = []

    # Compare each trait
    for trait in [

        "O",
        "C",
        "E",
        "A",
        "N"

    ]:

        # Candidate prediction
        candidate_value = predictions.get(
            trait
        )

        # Expected role value
        expected_value = required_personality.get(
            trait
        )

        # Skip unavailable predictions
        if candidate_value is None:

            continue

        # Compare values
        if int(candidate_value) == int(
            expected_value
        ):

            matching_traits.append(
                trait
            )

        else:

            mismatching_traits.append(
                trait
            )

    # Calculate personality score
    total_traits = len(
        matching_traits
    ) + len(
        mismatching_traits
    )

    if total_traits == 0:

        personality_score = 0.0

    else:

        personality_score = (

            len(matching_traits)
            / total_traits

        ) * 100

    return {

        "score": round(
            personality_score,
            2
        ),

        "matching_traits": matching_traits,

        "mismatching_traits": mismatching_traits

    }


# ============================================================
# 7. CALCULATE OVERALL ROLE MATCH
# ============================================================

def calculate_overall_score(
    skill_score,
    personality_score
):
    """
    Calculate final career-role match score.

    Weighting:
        Skills       = 70%
        Personality  = 30%

    Skills receive higher weight because career suitability
    should primarily depend on demonstrated capabilities.
    """

    overall_score = (

        (skill_score * 0.70)

        +

        (personality_score * 0.30)

    )

    return round(
        overall_score,
        2
    )


# ============================================================
# 8. MATCH ONE CAREER ROLE
# ============================================================

def match_career_role(
    candidate_skills,
    predictions,
    role_name,
    role_data
):
    """
    Calculate complete matching information for one role.
    """

    # Calculate skill compatibility
    skill_result = calculate_skill_match(

        candidate_skills,

        role_data["skills"]

    )

    # Calculate personality compatibility
    personality_result = calculate_personality_match(

        predictions,

        role_data["personality"]

    )

    # Calculate overall score
    overall_score = calculate_overall_score(

        skill_result["score"],

        personality_result["score"]

    )

    # Return complete role analysis
    return {

        "role": role_name,

        "overall_score": overall_score,

        "skill_score": skill_result[
            "score"
        ],

        "personality_score": personality_result[
            "score"
        ],

        "matched_skills": skill_result[
            "matched_skills"
        ],

        "missing_skills": skill_result[
            "missing_skills"
        ],

        "matching_traits": personality_result[
            "matching_traits"
        ],

        "mismatching_traits": personality_result[
            "mismatching_traits"
        ]

    }


# ============================================================
# 9. MATCH ALL CAREER ROLES
# ============================================================

def match_all_careers(
    skill_result,
    prediction_result
):
    """
    Match the candidate against every available career role.

    Returns
    -------
    list
        Ranked career matches.
    """

    # Prepare candidate skills
    candidate_skills = prepare_candidate_skills(
        skill_result
    )

    # Get personality predictions
    predictions = prediction_result.get(
        "predictions",
        {}
    )

    # Store results
    career_matches = []

    # Evaluate every role
    for role_name, role_data in CAREER_ROLES.items():

        result = match_career_role(

            candidate_skills,

            predictions,

            role_name,

            role_data

        )

        career_matches.append(
            result
        )

    # Sort highest score first
    career_matches.sort(

        key=lambda item:
        item["overall_score"],

        reverse=True

    )

    return career_matches


# ============================================================
# 10. GET TOP CAREER RECOMMENDATIONS
# ============================================================

def get_top_careers(
    career_matches,
    top_n=5
):
    """
    Return the highest-ranked career recommendations.
    """

    # Return requested number of roles
    return career_matches[
        :top_n
    ]


# ============================================================
# 11. CREATE CAREER SUMMARY
# ============================================================

def create_career_summary(
    career_matches,
    top_n=3
):
    """
    Create a concise career recommendation summary.
    """

    # Get top careers
    top_careers = get_top_careers(

        career_matches,

        top_n

    )

    # Create summary list
    summary = []

    # Build readable summaries
    for rank, career in enumerate(

        top_careers,

        start=1

    ):

        summary.append({

            "rank": rank,

            "role": career["role"],

            "match_score": career[
                "overall_score"
            ],

            "skill_score": career[
                "skill_score"
            ],

            "personality_score": career[
                "personality_score"
            ],

            "matched_skills": career[
                "matched_skills"
            ],

            "missing_skills": career[
                "missing_skills"
            ]

        })

    return summary


# ============================================================
# 12. COMPLETE CAREER ANALYSIS
# ============================================================

def analyze_career_fit(
    skill_result,
    prediction_result,
    top_n=5
):
    """
    Run the complete dynamic career matching pipeline.

    Parameters
    ----------
    skill_result : dict
        Output from skill_extractor.py.

    prediction_result : dict
        Output from personality_predictor.py.

    top_n : int
        Number of recommendations to return.

    Returns
    -------
    dict
        Complete career analysis.
    """

    # Match candidate with all roles
    career_matches = match_all_careers(

        skill_result,

        prediction_result

    )

    # Get top recommendations
    top_careers = get_top_careers(

        career_matches,

        top_n

    )

    # Create readable summary
    summary = create_career_summary(

        career_matches,

        top_n

    )

    return {

        "all_matches": career_matches,

        "top_careers": top_careers,

        "summary": summary

    }


# ============================================================
# 13. MODULE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Example candidate skills
    # --------------------------------------------------------

    sample_skills = {

        "total_skills": 15,

        "all_skills": [

            "Python",
            "Machine Learning",
            "Deep Learning",
            "Data Analysis",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Flask",
            "SQL",
            "Power BI",
            "Excel",
            "Dashboard Development",
            "Git",
            "GitHub",
            "Streamlit"

        ]

    }

    # --------------------------------------------------------
    # Example personality predictions
    # --------------------------------------------------------

    sample_predictions = {

        "predictions": {

            "O": 1,
            "C": 1,
            "E": 0,
            "A": 1,
            "N": 0

        }

    }

    # --------------------------------------------------------
    # Run career matching
    # --------------------------------------------------------

    result = analyze_career_fit(

        sample_skills,

        sample_predictions,

        top_n=5

    )

    # --------------------------------------------------------
    # Display success message
    # --------------------------------------------------------

    print(
        "Career matcher module loaded successfully."
    )

    # --------------------------------------------------------
    # Display top career recommendations
    # --------------------------------------------------------

    print(
        "\nTop Career Recommendations:"
    )

    print(
        "=" * 60
    )

    for career in result[
        "summary"
    ]:

        print(
            f"\n{career['rank']}. "
            f"{career['role']}"
        )

        print(
            f"   Overall Match: "
            f"{career['match_score']:.2f}%"
        )

        print(
            f"   Skill Match: "
            f"{career['skill_score']:.2f}%"
        )

        print(
            f"   Personality Match: "
            f"{career['personality_score']:.2f}%"
        )

        print(
            "   Matched Skills:",
            ", ".join(
                career["matched_skills"]
            )
        )

        print(
            "   Missing Skills:",
            ", ".join(
                career["missing_skills"]
            )
        )