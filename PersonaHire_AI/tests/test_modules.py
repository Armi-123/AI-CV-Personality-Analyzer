# ============================================================
# PERSONAHIRE AI
# PROJECT MODULE TESTS
# ============================================================

"""
Basic validation tests for PersonaHire AI.

These tests verify that the main project modules can be
imported and that the core text-processing components
produce valid outputs.

Run from the PersonaHire_AI project root:

    python tests/test_modules.py
"""
# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

import sys
from pathlib import Path

# Get the PersonaHire_AI project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Add project root to Python import path
sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

# ============================================================
# 1. IMPORT REQUIRED MODULES
# ============================================================

from src.text_preprocessor import (
    preprocess_cv_text,
    get_text_statistics
)

from src.skill_extractor import (
    analyze_cv_skills
)


# ============================================================
# 2. SAMPLE CV TEXT
# ============================================================

sample_cv_text = """
Armi Sherathiya

AI/ML Engineer and Data Scientist.

Skills:
Python, SQL, Pandas, NumPy, Scikit-learn,
Machine Learning, Power BI, Excel, Git,
GitHub, Streamlit.

Experience:
Python Developer Intern.
Built machine learning and data analytics
projects using Python and SQL.

Education:
M.Tech in Artificial Intelligence and
Machine Learning.
"""


# ============================================================
# 3. TEST TEXT PREPROCESSING
# ============================================================

print("\n" + "=" * 60)
print("TEST 1: TEXT PREPROCESSING")
print("=" * 60)

processed_text, statistics = preprocess_cv_text(
    sample_cv_text
)

assert processed_text
assert isinstance(
    processed_text,
    str
)

assert isinstance(
    statistics,
    dict
)

print(
    "Text preprocessing: PASSED"
)


# ============================================================
# 4. TEST TEXT STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("TEST 2: TEXT STATISTICS")
print("=" * 60)

required_statistics = [

    "character_count",
    "word_count",
    "sentence_count",
    "average_word_length",
    "uppercase_ratio",
    "digit_ratio",
    "punctuation_ratio"

]

for feature in required_statistics:

    assert feature in statistics

print(
    "All seven statistical features: PASSED"
)


# ============================================================
# 5. DISPLAY STATISTICS
# ============================================================

print("\nText Statistics:")

for feature, value in statistics.items():

    print(
        f"- {feature}: {value}"
    )


# ============================================================
# 6. TEST SKILL EXTRACTION
# ============================================================

print("\n" + "=" * 60)
print("TEST 3: SKILL EXTRACTION")
print("=" * 60)

skill_result = analyze_cv_skills(
    processed_text
)

assert isinstance(
    skill_result,
    dict
)

assert "all_skills" in skill_result

assert "skills_by_category" in skill_result

assert "total_skills" in skill_result

assert isinstance(
    skill_result["all_skills"],
    list
)

print(
    "Skill extraction: PASSED"
)


# ============================================================
# 7. DISPLAY DETECTED SKILLS
# ============================================================

print("\nDetected Skills:")

for skill in skill_result[
    "all_skills"
]:

    print(
        f"- {skill}"
    )


# ============================================================
# 8. FINAL TEST RESULT
# ============================================================

print("\n" + "=" * 60)
print("ALL BASIC PROJECT TESTS PASSED")
print("=" * 60)

print(
    "\nPersonaHire AI core modules are functioning correctly."
)