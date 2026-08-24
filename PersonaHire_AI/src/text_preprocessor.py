# ============================================================
# TEXT PREPROCESSOR
# AI CV Personality Analyzer
# ============================================================

"""
This module preprocesses CV/resume text before feature extraction.

Responsibilities:
    1. Validate extracted CV text.
    2. Normalize text.
    3. Remove unnecessary characters.
    4. Normalize whitespace.
    5. Preserve useful information required by the trained
       TF-IDF and statistical feature pipeline.

Important:
    The preprocessing must not aggressively remove information
    because the trained feature pipeline depends on the original
    text characteristics.
"""


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# Import regular expressions
import re


# ============================================================
# 2. BASIC TEXT VALIDATION
# ============================================================

def validate_text(text):
    """
    Validate extracted CV text.

    Parameters
    ----------
    text : str
        Extracted CV text.

    Returns
    -------
    bool
        True when usable text is available.
    """

    # Check whether text exists
    if text is None:
        return False

    # Convert to string
    text = str(text)

    # Remove surrounding whitespace
    text = text.strip()

    # Make sure meaningful text remains
    if len(text) == 0:
        return False

    return True


# ============================================================
# 3. NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    """
    Normalize extracted CV text.

    The function:
        - Converts repeated whitespace.
        - Normalizes line breaks.
        - Removes unnecessary control characters.
        - Preserves words, numbers and punctuation.
    """

    # Validate input
    if not validate_text(text):
        raise ValueError(
            "No valid CV text was provided."
        )

    # Convert to string
    text = str(text)

    # Normalize Windows line endings
    text = text.replace(
        "\r\n",
        "\n"
    )

    # Normalize remaining carriage returns
    text = text.replace(
        "\r",
        "\n"
    )

    # Remove non-printable control characters
    text = re.sub(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
        " ",
        text
    )

    # Replace tabs with spaces
    text = text.replace(
        "\t",
        " "
    )

    # Remove excessive spaces
    text = re.sub(
        r" {2,}",
        " ",
        text
    )

    # Remove spaces at the beginning of lines
    text = re.sub(
        r"\n +",
        "\n",
        text
    )

    # Remove spaces at the end of lines
    text = re.sub(
        r" +\n",
        "\n",
        text
    )

    # Reduce excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # Remove unnecessary leading/trailing whitespace
    text = text.strip()

    return text


# ============================================================
# 4. PREPROCESS CV TEXT
# ============================================================

def preprocess_text(text):
    """
    Main preprocessing function used by the application.

    Parameters
    ----------
    text : str
        Raw text extracted from a CV.

    Returns
    -------
    str
        Cleaned CV text.
    """

    # Validate the extracted text
    if not validate_text(text):

        raise ValueError(
            "CV text is empty or invalid."
        )

    # Normalize the extracted text
    processed_text = normalize_text(
        text
    )

    # Final validation
    if not processed_text:

        raise ValueError(
            "No usable text remains after preprocessing."
        )

    return processed_text


# ============================================================
# 5. GET BASIC TEXT STATISTICS
# ============================================================

def get_text_statistics(text):
    """
    Calculate the seven statistical features used by the
    feature-engineering pipeline.

    Features:
        - character_count
        - word_count
        - sentence_count
        - average_word_length
        - uppercase_ratio
        - digit_ratio
        - punctuation_ratio

    Parameters
    ----------
    text : str
        Preprocessed CV text.

    Returns
    -------
    dict
        Dictionary containing the seven text statistics.
    """

    # Validate text
    if not validate_text(text):

        raise ValueError(
            "Cannot calculate statistics from empty text."
        )

    # Convert text to string
    text = str(text)

    # --------------------------------------------------------
    # Character count
    # --------------------------------------------------------

    character_count = len(text)

    # --------------------------------------------------------
    # Word extraction
    # --------------------------------------------------------

    words = re.findall(
        r"\b\w+\b",
        text
    )

    # Count words
    word_count = len(words)

    # --------------------------------------------------------
    # Sentence count
    # --------------------------------------------------------

    sentences = re.split(
        r"[.!?]+",
        text
    )

    # Remove empty sentences
    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = len(
        sentences
    )

    # Avoid division by zero
    if word_count > 0:

        # Calculate average word length
        total_word_length = sum(
            len(word)
            for word in words
        )

        average_word_length = (
            total_word_length
            / word_count
        )

    else:

        average_word_length = 0.0

    # --------------------------------------------------------
    # Uppercase ratio
    # --------------------------------------------------------

    alphabetic_characters = [
        character
        for character in text
        if character.isalpha()
    ]

    if alphabetic_characters:

        uppercase_characters = [
            character
            for character in alphabetic_characters
            if character.isupper()
        ]

        uppercase_ratio = (
            len(uppercase_characters)
            / len(alphabetic_characters)
        )

    else:

        uppercase_ratio = 0.0

    # --------------------------------------------------------
    # Digit ratio
    # --------------------------------------------------------

    if character_count > 0:

        digit_count = sum(
            character.isdigit()
            for character in text
        )

        digit_ratio = (
            digit_count
            / character_count
        )

    else:

        digit_ratio = 0.0

    # --------------------------------------------------------
    # Punctuation ratio
    # --------------------------------------------------------

    if character_count > 0:

        punctuation_count = sum(
            character in ".,!?;:'\"-()[]{}"
            for character in text
        )

        punctuation_ratio = (
            punctuation_count
            / character_count
        )

    else:

        punctuation_ratio = 0.0

    # --------------------------------------------------------
    # Return all seven features
    # --------------------------------------------------------

    return {
        "character_count": character_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_word_length": average_word_length,
        "uppercase_ratio": uppercase_ratio,
        "digit_ratio": digit_ratio,
        "punctuation_ratio": punctuation_ratio
    }


# ============================================================
# 6. PREPROCESS AND CALCULATE STATISTICS
# ============================================================

def preprocess_cv_text(text):
    """
    Complete preprocessing pipeline.

    Returns both:
        1. Cleaned CV text
        2. Seven statistical features

    This function will be useful when connecting the parser
    with the feature-generation module.
    """

    # Clean the CV text
    processed_text = preprocess_text(
        text
    )

    # Calculate statistical features
    statistics = get_text_statistics(
        processed_text
    )

    return (
        processed_text,
        statistics
    )


# ============================================================
# 7. MODULE TEST
# ============================================================

if __name__ == "__main__":

    # Example CV text for testing
    sample_text = """
    Armi Sherathiya
    AI/ML Engineer

    Skills:
    Python, SQL, Machine Learning, Power BI

    Experience:
    Python Developer Intern
    """

    # Run preprocessing
    cleaned_text, statistics = preprocess_cv_text(
        sample_text
    )

    # Display results
    print(
        "Text preprocessing module loaded successfully."
    )

    print("\nCleaned Text:")
    print(cleaned_text)

    print("\nText Statistics:")

    for feature, value in statistics.items():

        print(
            f"{feature}: {value}"
        )