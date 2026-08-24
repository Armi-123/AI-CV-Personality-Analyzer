# ============================================================
# PERSONALITY PREDICTOR
# AI CV Personality Analyzer
# ============================================================

"""
This module connects the trained Machine Learning pipeline
with a new candidate CV.

Pipeline:

    CV Text
       ↓
    Word TF-IDF
       ↓
    Character TF-IDF
       ↓
    Text Statistics
       ↓
    Combined Feature Matrix
       ↓
    Five Personality Models
       ↓
    O / C / E / A / N Predictions


The trained feature pipeline contains:

    Word TF-IDF       : 20,000 features
    Character TF-IDF  : 15,000 features
    Text Statistics   : 7 features
    --------------------------------
    Total             : 35,007 features
"""


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# Import os for file path handling
import os

# Import joblib for loading saved vectorizers, scalers and models
import joblib

# Import NumPy for numerical operations
import numpy as np

# Import pandas for handling feature tables

import pandas as pd

# Import sparse matrix utilities
from scipy.sparse import hstack, csr_matrix


# ============================================================
# 2. IMPORT PROJECT PREPROCESSOR
# ============================================================

try:

    from src.text_preprocessor import preprocess_cv_text

except ModuleNotFoundError:

    from text_preprocessor import preprocess_cv_text


# ============================================================
# 3. PROJECT PATH CONFIGURATION
# ============================================================

# Get the directory containing this Python file
CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# Move one level up from src/
# to reach the main PersonaHire_AI project directory
PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)


# Define the models directory
MODELS_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)


# ============================================================
# 4. FEATURE ARTIFACT PATHS
# ============================================================

# Word-level TF-IDF vectorizer
WORD_TFIDF_PATH = os.path.join(
    MODELS_DIR,
    "word_tfidf_vectorizer.pkl"
)


# Character-level TF-IDF vectorizer
CHAR_TFIDF_PATH = os.path.join(
    MODELS_DIR,
    "char_tfidf_vectorizer.pkl"
)


# Statistical feature scaler
STATS_SCALER_PATH = os.path.join(
    MODELS_DIR,
    "text_stats_scaler.pkl"
)


# ============================================================
# 5. PERSONALITY MODEL PATHS
# ============================================================

# Big Five personality model files
MODEL_PATHS = {

    "O": os.path.join(
        MODELS_DIR,
        "personality_model_O.pkl"
    ),

    "C": os.path.join(
        MODELS_DIR,
        "personality_model_C.pkl"
    ),

    "E": os.path.join(
        MODELS_DIR,
        "personality_model_E.pkl"
    ),

    "A": os.path.join(
        MODELS_DIR,
        "personality_model_A.pkl"
    ),

    "N": os.path.join(
        MODELS_DIR,
        "personality_model_N.pkl"
    )
}


# ============================================================
# 6. HUMAN-READABLE TRAIT NAMES
# ============================================================

TRAIT_NAMES = {

    "O": "Openness",

    "C": "Conscientiousness",

    "E": "Extraversion",

    "A": "Agreeableness",

    "N": "Neuroticism"
}


# ============================================================
# 7. LOAD TRAINED ARTIFACTS
# ============================================================

def load_artifacts():
    """
    Load all trained feature-processing artifacts and
    personality prediction models.

    Returns
    -------
    dict
        Dictionary containing vectorizers, scaler and models.
    """

    # --------------------------------------------------------
    # Check whether the models directory exists
    # --------------------------------------------------------

    if not os.path.exists(MODELS_DIR):

        raise FileNotFoundError(
            f"Models directory not found: {MODELS_DIR}"
        )


    # --------------------------------------------------------
    # Check required feature artifacts
    # --------------------------------------------------------

    required_files = [

        WORD_TFIDF_PATH,

        CHAR_TFIDF_PATH,

        STATS_SCALER_PATH

    ]


    # Add all five personality model paths
    required_files.extend(
        MODEL_PATHS.values()
    )


    # Check every required file
    for file_path in required_files:

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"Required model artifact not found: "
                f"{file_path}"
            )


    # --------------------------------------------------------
    # Load Word TF-IDF vectorizer
    # --------------------------------------------------------

    word_vectorizer = joblib.load(
        WORD_TFIDF_PATH
    )


    # --------------------------------------------------------
    # Load Character TF-IDF vectorizer
    # --------------------------------------------------------

    char_vectorizer = joblib.load(
        CHAR_TFIDF_PATH
    )


    # --------------------------------------------------------
    # Load statistical feature scaler
    # --------------------------------------------------------

    stats_scaler = joblib.load(
        STATS_SCALER_PATH
    )


    # --------------------------------------------------------
    # Load five personality models
    # --------------------------------------------------------

    personality_models = {}

    for trait, model_path in MODEL_PATHS.items():

        personality_models[trait] = joblib.load(
            model_path
        )


    # --------------------------------------------------------
    # Return all loaded artifacts
    # --------------------------------------------------------

    return {

        "word_vectorizer": word_vectorizer,

        "char_vectorizer": char_vectorizer,

        "stats_scaler": stats_scaler,

        "personality_models": personality_models

    }


# ============================================================
# 8. GENERATE FEATURE MATRIX
# ============================================================

def generate_features(
    text,
    artifacts
):
    """
    Convert new CV text into the same feature representation
    used during model training.

    Feature structure:

        Word TF-IDF       = 20,000
        Character TF-IDF  = 15,000
        Statistics        = 7

        Total             = 35,007

    Parameters
    ----------
    text : str
        Raw or extracted CV text.

    artifacts : dict
        Loaded vectorizers and scaler.

    Returns
    -------
    scipy.sparse matrix
        Combined feature matrix.
    """

    # --------------------------------------------------------
    # Preprocess CV text
    # --------------------------------------------------------

    processed_text, statistics = preprocess_cv_text(
        text
    )


    # --------------------------------------------------------
    # Word-level TF-IDF
    # --------------------------------------------------------

    word_features = artifacts[
        "word_vectorizer"
    ].transform(
        [processed_text]
    )


    # --------------------------------------------------------
    # Character-level TF-IDF
    # --------------------------------------------------------

    char_features = artifacts[
        "char_vectorizer"
    ].transform(
        [processed_text]
    )


    # --------------------------------------------------------
    # Convert statistics into DataFrame
    # --------------------------------------------------------

    statistics_df = pd.DataFrame(
        [statistics]
    )


    # --------------------------------------------------------
    # Ensure the statistical feature order
    # matches the training pipeline
    # --------------------------------------------------------

    statistical_columns = [

        "character_count",

        "word_count",

        "sentence_count",

        "average_word_length",

        "uppercase_ratio",

        "digit_ratio",

        "punctuation_ratio"

    ]


    statistics_df = statistics_df[
        statistical_columns
    ]


    # --------------------------------------------------------
    # Scale statistical features
    # --------------------------------------------------------

    scaled_statistics = artifacts[
        "stats_scaler"
    ].transform(
        statistics_df
    )


    # --------------------------------------------------------
    # Convert statistical features to sparse format
    # --------------------------------------------------------

    statistics_sparse = csr_matrix(
        scaled_statistics
    )


    # --------------------------------------------------------
    # Combine all feature groups
    # --------------------------------------------------------

    combined_features = hstack(

        [

            word_features,

            char_features,

            statistics_sparse

        ],

        format="csr"

    )


    # --------------------------------------------------------
    # Verify final feature count
    # --------------------------------------------------------

    expected_features = 35007

    if combined_features.shape[1] != expected_features:

        raise ValueError(

            "Feature dimension mismatch. "
            f"Expected {expected_features} features, "
            f"but generated "
            f"{combined_features.shape[1]}."

        )


    return combined_features


# ============================================================
# 9. PREDICT PERSONALITY TRAITS
# ============================================================

def predict_personality(
    text,
    artifacts=None
):
    """
    Predict the Big Five personality traits for a new CV.

    Parameters
    ----------
    text : str
        Extracted CV text.

    artifacts : dict, optional
        Previously loaded artifacts.

    Returns
    -------
    dict
        Personality prediction results.
    """

    # --------------------------------------------------------
    # Load artifacts if they were not supplied
    # --------------------------------------------------------

    if artifacts is None:

        artifacts = load_artifacts()


    # --------------------------------------------------------
    # Generate the 35,007-feature representation
    # --------------------------------------------------------

    feature_matrix = generate_features(

        text,

        artifacts

    )


    # --------------------------------------------------------
    # Store prediction results
    # --------------------------------------------------------

    predictions = {}


    # Store probability/confidence values when available
    confidence_scores = {}


    # --------------------------------------------------------
    # Predict each Big Five personality trait
    # --------------------------------------------------------

    for trait in [

        "O",
        "C",
        "E",
        "A",
        "N"

    ]:

        # Get corresponding trained model
        model = artifacts[
            "personality_models"
        ][trait]


        # Generate prediction
        prediction = model.predict(
            feature_matrix
        )[0]


        # Convert prediction to integer
        prediction = int(
            prediction
        )


        # Store prediction
        predictions[trait] = prediction


        # ----------------------------------------------------
        # Calculate confidence when supported
        # ----------------------------------------------------

        if hasattr(
            model,
            "predict_proba"
        ):

            probabilities = model.predict_proba(
                feature_matrix
            )[0]

            # Maximum probability as confidence
            confidence = float(
                np.max(probabilities)
            )

            confidence_scores[trait] = confidence


        elif hasattr(
            model,
            "decision_function"
        ):

            decision_score = model.decision_function(
                feature_matrix
            )[0]


            # Convert decision score approximately
            # into a probability-like confidence score
            confidence = 1 / (
                1 + np.exp(
                    -abs(decision_score)
                )
            )


            confidence_scores[trait] = float(
                confidence
            )


        else:

            confidence_scores[trait] = None


    # --------------------------------------------------------
    # Convert predictions to human-readable labels
    # --------------------------------------------------------

    personality_results = {}


    for trait in [

        "O",
        "C",
        "E",
        "A",
        "N"

    ]:

        personality_results[
            TRAIT_NAMES[trait]
        ] = {

            "label": predictions[trait],

            "confidence": confidence_scores[trait]

        }


    # --------------------------------------------------------
    # Return complete result
    # --------------------------------------------------------

    return {

        "predictions": predictions,

        "confidence": confidence_scores,

        "traits": personality_results

    }


# ============================================================
# 10. CREATE SIMPLE PERSONALITY SUMMARY
# ============================================================

def create_personality_summary(
    prediction_result
):
    """
    Convert binary personality predictions into a readable
    summary.

    Parameters
    ----------
    prediction_result : dict
        Result returned by predict_personality().

    Returns
    -------
    dict
        Human-readable personality summary.
    """

    predictions = prediction_result[
        "predictions"
    ]


    summary = {}


    for trait, label in predictions.items():

        trait_name = TRAIT_NAMES[
            trait
        ]


        if label == 1:

            interpretation = (
                f"Higher predicted {trait_name}"
            )

        else:

            interpretation = (
                f"Lower predicted {trait_name}"
            )


        summary[trait_name] = interpretation


    return summary


# ============================================================
# 11. COMPLETE PREDICTION PIPELINE
# ============================================================

def analyze_cv_personality(
    text
):
    """
    Run the complete personality prediction pipeline.

    Parameters
    ----------
    text : str
        Extracted CV text.

    Returns
    -------
    dict
        Complete personality analysis.
    """

    # Load all trained artifacts
    artifacts = load_artifacts()


    # Predict personality traits
    prediction_result = predict_personality(

        text,

        artifacts

    )


    # Generate readable summary
    summary = create_personality_summary(
        prediction_result
    )


    # Add summary to result
    prediction_result[
        "summary"
    ] = summary


    return prediction_result


# ============================================================
# 12. MODULE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "Personality predictor module loaded successfully."
    )

    print(
        f"Models directory: {MODELS_DIR}"
    )

    print(
        "\nExpected feature count: 35,007"
    )

    print(
        "\nBig Five personality models:"
    )

    for trait, name in TRAIT_NAMES.items():

        print(
            f"- {trait}: {name}"
        )