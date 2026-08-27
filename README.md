# 🧠 PersonaHire AI – AI-Powered CV Personality & Career Analyzer

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-green)

PersonaHire AI is an **AI/ML-powered CV personality and career analysis system** that analyzes candidate resumes to predict **Big Five personality traits**, extract professional skills, and recommend suitable career roles.

The system supports **PDF and DOCX CV uploads** and processes each candidate through an end-to-end machine learning pipeline including text extraction, preprocessing, feature engineering, personality prediction, skill extraction, career matching, and automated report generation.

This project demonstrates the practical implementation of **Machine Learning, Natural Language Processing, TF-IDF feature engineering, text analysis, and Streamlit application development**.

---

# 📌 Features

### 📄 CV Processing

- PDF CV upload and text extraction
- DOCX CV upload and text extraction
- Automated CV text preprocessing
- Text validation and normalization

### 🧠 Personality Analysis

- Big Five personality prediction
- Openness prediction
- Conscientiousness prediction
- Extraversion prediction
- Agreeableness prediction
- Neuroticism prediction
- Personality confidence analysis

### 🛠️ Skill Extraction

- Automatic professional skill extraction
- Technical skill detection
- Skill categorization
- Programming and data science skill identification
- Business intelligence and analytics skill detection

### 💼 Career Matching

- Career role recommendations
- Overall career match score
- Skill match score
- Personality match score
- Matched skills identification
- Skills-to-improve identification

### 📊 Candidate Dashboard

- Candidate overview
- Total extracted skills
- Career roles analyzed
- Top career match
- Big Five personality visualization
- Skill categorization
- Career recommendation ranking
- Executive candidate summary

### 📄 Report Generation

- Automated candidate report generation
- Personality analysis report
- Extracted skills report
- Career recommendation report
- Executive summary
- Downloadable candidate report

### 🧪 Testing

- Text preprocessing testing
- Text statistics testing
- Skill extraction testing
- Core module verification

---

# 🧠 Big Five Personality Analysis

PersonaHire AI predicts five major personality dimensions based on CV text.

| Trait | Meaning |
|---|---|
| **O — Openness** | Creativity, curiosity, and openness to new experiences |
| **C — Conscientiousness** | Organization, responsibility, and discipline |
| **E — Extraversion** | Social interaction, communication, and energy |
| **A — Agreeableness** | Cooperation, empathy, and interpersonal orientation |
| **N — Neuroticism** | Emotional sensitivity and emotional reactivity |

Each personality trait is analyzed independently using trained machine learning models.

---

# 🔄 System Workflow

```text
                    Candidate CV
                         │
                         ▼
                 PDF / DOCX Upload
                         │
                         ▼
                  Text Extraction
                         │
                         ▼
                 Text Preprocessing
                         │
                         ▼
                Feature Engineering
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Word TF-IDF   Character TF-IDF   Text Statistics
       20,000          15,000              7
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  35,007 Features
                         │
                         ▼
              Personality Prediction
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
          O              C              E
      Openness     Conscientiousness  Extraversion
          │              │              │
          └──────────────┼──────────────┘
                         │
                    A + N Traits
                         │
                         ▼
                  Skill Extraction
                         │
                         ▼
                  Career Matching
                         │
                         ▼
                Candidate Analysis
                         │
                         ▼
                 Report Generation
```

---

# 🧮 Feature Engineering

The personality prediction pipeline uses **35,007 features**.

| Feature Type | Number of Features |
|---|---:|
| Word-level TF-IDF | 20,000 |
| Character-level TF-IDF | 15,000 |
| Text Statistical Features | 7 |
| **Total** | **35,007** |

### Text Statistical Features

The system extracts:

- Character count
- Word count
- Sentence count
- Average word length
- Uppercase ratio
- Digit ratio
- Punctuation ratio

---

# 🤖 Machine Learning

The system uses machine learning classification models to independently predict the five Big Five personality traits.

### Prediction Targets

```text
O → Openness
C → Conscientiousness
E → Extraversion
A → Agreeableness
N → Neuroticism
```

The trained models and feature-processing artifacts are loaded dynamically during candidate CV analysis.

---

# 🛠️ Skill Extraction

PersonaHire AI automatically identifies professional and technical skills from uploaded CVs.

### Skill Categories

```text
Programming Languages
Data Science & Machine Learning
Python & Data Libraries
Web Development
Databases
Business Intelligence & Analytics
Tools & Technologies
```

### Example Detected Skills

```text
Python
SQL
Machine Learning
Pandas
NumPy
Scikit-learn
Power BI
Excel
Git
GitHub
Streamlit
```

The extracted skills are used during the career matching stage.

---

# 💼 Career Matching

The application analyzes the relationship between:

- Candidate skills
- Personality predictions
- Career requirements

and generates career suitability scores.

### Example Career Roles

- Data Scientist
- Data Analyst
- Business Analyst
- Python Developer
- Machine Learning Engineer

For each recommended role, the system provides:

- Overall Match
- Skill Match
- Personality Match
- Matched Skills
- Skills to Improve

---

# 📊 Candidate Analysis Dashboard

The Streamlit application provides an interactive candidate analysis dashboard.

### Candidate Overview

- Total Skills
- Career Roles Analyzed
- Top Career Match

### Personality Analysis

Displays predicted Big Five personality traits and their confidence scores.

### Skills Analysis

Displays:

- Total extracted skills
- Individual extracted skills
- Skills grouped by category

### Career Recommendations

Displays ranked career roles with:

- Overall match percentage
- Skill match percentage
- Personality match percentage
- Matched skills
- Skills to improve

### Executive Summary

Provides a concise summary of the candidate's overall analysis.

---

# 📄 Candidate Report

After completing the CV analysis, PersonaHire AI generates a downloadable candidate report containing:

- Candidate information
- Analysis timestamp
- Executive summary
- Big Five personality analysis
- Personality confidence scores
- Extracted skills
- Skill categories
- Career recommendations

The generated report can be downloaded directly from the Streamlit application.

---

# 📊 Dataset

The personality prediction model was developed using the **Essays Big Five personality dataset**.

The dataset contains text samples with labels for the five personality traits:

```text
O → Openness
C → Conscientiousness
E → Extraversion
A → Agreeableness
N → Neuroticism
```

### Dataset Split

| Dataset | Records |
|---|---:|
| Training | 1,578 |
| Validation | 395 |
| Test | 494 |
| **Total** | **2,467** |

### Dataset Features

The dataset contains:

```text
O
C
E
A
N
ptype
text
__index_level_0__
```

The raw dataset is stored locally and excluded from Git tracking through `.gitignore`.

---

# 📁 Project Structure

```text
PersonaHire_AI/
│
├── data/
│   └── raw/
│
├── models/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_model_evaluation.ipynb
│
├── reports/
│
├── src/
│   ├── career_matcher.py
│   ├── docx_parser.py
│   ├── pdf_parser.py
│   ├── personality_predictor.py
│   ├── report_generator.py
│   ├── skill_extractor.py
│   └── text_preprocessor.py
│
├── tests/
│   └── test_modules.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧰 Technologies Used

### Programming

- Python 3

### Data Processing

- Pandas
- NumPy

### Machine Learning

- Scikit-learn
- Joblib

### Natural Language Processing

- TF-IDF
- Text preprocessing
- Text statistical analysis

### Visualization

- Matplotlib
- Seaborn
- Plotly

### Web Application

- Streamlit

### Document Processing

- PyPDF
- python-docx

### Development Tools

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/Armi-123/AI-CV-Personality-Analyzer.git
```

Go to the project directory:

```bash
cd AI-CV-Personality-Analyzer
```

---

## Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

### Application Workflow

1. Upload a candidate CV in PDF or DOCX format.
2. Extract the CV text.
3. Preprocess the extracted text.
4. Generate the required feature representation.
5. Predict the Big Five personality traits.
6. Extract professional skills.
7. Match the candidate with suitable career roles.
8. Generate the executive summary.
9. Generate and download the candidate report.

---

# 🧪 Testing

Core project modules can be tested using:

```bash
python tests/test_modules.py
```

The test validates:

- Text preprocessing
- Text statistics
- Skill extraction
- Core module functionality

### Expected Result

```text
============================================================
TEST 1: TEXT PREPROCESSING
============================================================
Text preprocessing: PASSED

============================================================
TEST 2: TEXT STATISTICS
============================================================
All seven statistical features: PASSED

============================================================
TEST 3: SKILL EXTRACTION
============================================================
Skill extraction: PASSED

============================================================
ALL BASIC PROJECT TESTS PASSED
============================================================

PersonaHire AI core modules are functioning correctly.
```

---

# 🔐 Data & Privacy

Candidate CVs are processed locally by the application during analysis.

The downloaded dataset, generated reports, cached files, and other local artifacts are excluded from Git tracking where appropriate through `.gitignore`.

Do not commit:

- Private candidate CVs
- API keys
- Credentials
- Personal information
- Other sensitive files

to the public repository.

---

# ⚠️ Responsible Use

PersonaHire AI is an experimental AI/ML project intended for **educational, research, and decision-support purposes**.

Personality predictions from CV text may contain uncertainty and potential bias. The system should **not be used as the sole basis for employment, recruitment, or hiring decisions**.

Human review and additional candidate information should always be considered before making important decisions.

---

# 📖 Learning Outcomes

This project demonstrates practical implementation of:

- Machine Learning classification
- Natural Language Processing
- TF-IDF feature engineering
- Text statistical analysis
- Big Five personality prediction
- Resume/CV document processing
- Professional skill extraction
- Career recommendation systems
- Streamlit application development
- Automated report generation
- Modular Python development
- End-to-end AI/ML project deployment

---

# 🎯 Project Objective

The objective of PersonaHire AI is to demonstrate how machine learning and natural language processing can transform unstructured CV data into structured candidate insights.

```text
CV Text
   ↓
Personality Traits
   ↓
Professional Skills
   ↓
Career Suitability
   ↓
Candidate Report
```

The project demonstrates an end-to-end AI/ML workflow:

```text
Data Preparation
      ↓
Data Exploration
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Model Training
      ↓
Model Evaluation
      ↓
CV Processing
      ↓
Personality Prediction
      ↓
Skill Extraction
      ↓
Career Matching
      ↓
Report Generation
      ↓
Streamlit Deployment
```

---

# 🎓 Project Highlights

- **2,467** total personality dataset records
- **35,007** engineered features
- **5** Big Five personality traits
- **7** statistical text features
- **20,000** word-level TF-IDF features
- **15,000** character-level TF-IDF features
- PDF and DOCX CV support
- Automated skill extraction
- Career suitability analysis
- Interactive Streamlit dashboard
- Automated candidate report generation
- Core module testing

---

# 👨‍💻 Author

## Armi Sherathiya

**AI/ML Engineer | Data Scientist**

Interested in:

- Artificial Intelligence
- Machine Learning
- Data Science
- Python Development
- Generative AI
- Natural Language Processing

GitHub:

https://github.com/Armi-123

---

# 🤝 Contributing

Contributions, feature suggestions, and bug reports are welcome.

Feel free to fork this repository and submit a pull request.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# ⭐ Support

If you found this project useful, please consider giving the repository a **Star ⭐** on GitHub.

It helps support the project and encourages future development.

---
