# Resume Feedback Analyzer

An interactive web application built with Streamlit that analyzes a resume against a job description, providing instant feedback on matching and missing skills.

## Features

- **Resume Parsing:** Extracts text from PDF and DOCX files.
- **Skill Matching:** Identifies skills from a predefined list present in both the resume and job description.
- **Structured Feedback:** Provides clear, actionable feedback on strengths (matched skills) and areas for improvement (missing skills).

## Tech Stack

- **Python**
- **Streamlit:** For the user interface.
- **PyPDF2 & python-docx:** For resume text extraction.
- **spaCy:** For basic text processing and keyword analysis.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KrittikaDas/Resume-Feedback-Analyser.git
    cd resume-feedback-analyzer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download the `spaCy` model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```
5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    Your browser will automatically open the web app.

## Contributing

Feel free to open issues or submit pull requests to improve this project.
