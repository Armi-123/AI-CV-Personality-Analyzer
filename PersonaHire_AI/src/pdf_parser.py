# ============================================================
# PDF CV PARSER
# AI CV Personality Analyzer
# ============================================================

"""
This module extracts text from PDF CV/resume files.

Responsibilities:
    1. Validate the uploaded PDF file.
    2. Open the PDF safely.
    3. Extract text from every page.
    4. Combine the extracted text.
    5. Clean unnecessary whitespace.
    6. Return the extracted CV text.

This module does NOT:
    - Predict personality traits.
    - Extract skills.
    - Perform career matching.
    - Generate reports.

Those responsibilities are handled by separate modules.
"""

# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# Import regular expressions for text cleaning
import re

# Import PdfReader for reading PDF documents
from pypdf import PdfReader

# ============================================================
# 2. EXTRACT TEXT FROM PDF
# ============================================================

def extract_pdf_text(pdf_file):
    """
    Extract text from a PDF CV/resume.

    Parameters
    ----------
    pdf_file : str or file-like object
        Path to the PDF file or an uploaded PDF file object.

    Returns
    -------
    str
        Extracted and cleaned CV text.

    Raises
    ------
    ValueError
        If the file is empty, invalid, or contains no readable text.
    """

    # --------------------------------------------------------
    # Validate the input
    # --------------------------------------------------------

    if pdf_file is None:
        raise ValueError(
            "No PDF file was provided."
        )

    try:

        # ----------------------------------------------------
        # Create a PDF reader
        # ----------------------------------------------------

        reader = PdfReader(pdf_file)

    except Exception as error:

        raise ValueError(
            "Unable to read the PDF file. "
            "Please upload a valid PDF CV."
        ) from error

    # --------------------------------------------------------
    # Check whether the PDF contains pages
    # --------------------------------------------------------

    if len(reader.pages) == 0:

        raise ValueError(
            "The uploaded PDF does not contain any pages."
        )

    # --------------------------------------------------------
    # Extract text from every page
    # --------------------------------------------------------

    extracted_pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        try:

            # Extract text from the current page
            page_text = page.extract_text()

        except Exception:
            # Skip a page if text extraction fails
            page_text = ""

        # Only keep pages that contain readable text
        if page_text:

            extracted_pages.append(
                page_text
            )

    # --------------------------------------------------------
    # Check whether any text was extracted
    # --------------------------------------------------------

    if not extracted_pages:

        raise ValueError(
            "No readable text was found in the PDF. "
            "The CV may be scanned or image-based."
        )

    # --------------------------------------------------------
    # Combine text from all pages
    # --------------------------------------------------------

    full_text = "\n".join(
        extracted_pages
    )

    # --------------------------------------------------------
    # Clean the extracted text
    # --------------------------------------------------------

    full_text = clean_pdf_text(
        full_text
    )

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if not full_text.strip():

        raise ValueError(
            "The PDF was read successfully, "
            "but no usable text was found."
        )

    return full_text


# ============================================================
# 3. CLEAN EXTRACTED PDF TEXT
# ============================================================

def clean_pdf_text(text):
    """
    Clean text extracted from a PDF.

    Cleaning includes:
        - Removing excessive spaces.
        - Removing excessive blank lines.
        - Normalizing line breaks.
        - Removing non-printable characters.

    Parameters
    ----------
    text : str
        Raw extracted PDF text.

    Returns
    -------
    str
        Cleaned text.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not text:
        return ""

    # Convert input to string
    text = str(text)

    # --------------------------------------------------------
    # Remove non-printable control characters
    # --------------------------------------------------------

    text = re.sub(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
        " ",
        text
    )

    # --------------------------------------------------------
    # Normalize different types of line breaks
    # --------------------------------------------------------

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    # --------------------------------------------------------
    # Remove spaces before line breaks
    # --------------------------------------------------------

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )

    # --------------------------------------------------------
    # Remove excessive spaces and tabs
    # --------------------------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # --------------------------------------------------------
    # Remove excessive blank lines
    # --------------------------------------------------------

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # --------------------------------------------------------
    # Remove unnecessary spaces at the beginning/end
    # --------------------------------------------------------

    text = text.strip()

    return text


# ============================================================
# 4. GET PDF PAGE COUNT
# ============================================================

def get_pdf_page_count(pdf_file):
    """
    Return the number of pages in a PDF.

    Parameters
    ----------
    pdf_file : str or file-like object
        PDF file path or uploaded PDF object.

    Returns
    -------
    int
        Number of pages.
    """

    if pdf_file is None:

        raise ValueError(
            "No PDF file was provided."
        )

    try:

        # Create PDF reader
        reader = PdfReader(pdf_file)

        # Return number of pages
        return len(reader.pages)

    except Exception as error:

        raise ValueError(
            "Unable to determine the PDF page count."
        ) from error


# ============================================================
# 5. BASIC PDF VALIDATION
# ============================================================

def validate_pdf_file(pdf_file):
    """
    Validate whether the supplied file can be opened as a PDF.

    Parameters
    ----------
    pdf_file : str or file-like object
        PDF file path or uploaded PDF object.

    Returns
    -------
    bool
        True when the PDF is valid.
    """

    if pdf_file is None:

        return False

    try:

        # Try opening the PDF
        reader = PdfReader(pdf_file)

        # A valid PDF should contain at least one page
        return len(reader.pages) > 0

    except Exception:

        return False


# ============================================================
# 6. MODULE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "PDF parser module loaded successfully."
    )

    print(
        "Use extract_pdf_text() to extract text "
        "from a CV PDF."
    )