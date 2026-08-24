from src.text_preprocessor import preprocess_cv_text

sample_text = """
Armi Sherathiya
AI/ML Engineer
Python, SQL, Machine Learning
2 years of experience.
"""

cleaned_text, statistics = preprocess_cv_text(sample_text)

print("Cleaned Text:")
print(cleaned_text)

print("\nStatistics:")
print(statistics)