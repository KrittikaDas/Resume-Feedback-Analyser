# Resume Feedback Analyzer

An interactive web application that uses Generative AI to analyze a resume against a job description and provide structured feedback.

## Features

- **Resume Parsing:** Extracts text from PDF and DOCX files.
- **AI-Powered Analysis:** Leverages the Gemini API to intelligently compare a resume to a job description.
- **Structured Feedback:** Provides a match score and detailed feedback on strengths, missing skills, and improvements.

## Tech Stack

- **Python**
- **Streamlit:** For the user interface.
- **google-generativeai:** To connect with the Gemini API.
- **python-dotenv:** To securely manage the API key.
- **PyPDF2 & python-docx:** For resume text extraction.

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
4.  **Set up your Google API key:**
    * Go to [Google AI Studio](https://aistudio.google.com/app/apikey) to get your free API key.
    * Create a file named `.env` in the project's root folder.
    * Add your key to the file like this: `GOOGLE_API_KEY=your_key_here`.
5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    Your browser will automatically open the web app.

## Contributing

Feel free to open issues or submit pull requests to improve this project.






