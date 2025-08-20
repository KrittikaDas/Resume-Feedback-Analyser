import streamlit as st
import PyPDF2
from docx import Document
import google.generativeai as genai
import io
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    model = None

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(uploaded_file):
    text = ""
    try:
        doc = Document(io.BytesIO(uploaded_file.getvalue()))
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
    return text

# Function to analyze the resume against the job description using LLM
def analyze_resume_with_llm(resume_text, job_description_text):
    if not model:
        return None

    prompt = f"""
    You are an AI career coach. Your task is to analyze a candidate's resume against a specific job description.

    Provide a structured JSON output with the following keys:
    "matched_skills": a list of skills from the job description that are present in the resume.
    "missing_skills": a list of key skills from the job description that are NOT in the resume.
    "strengths": a short paragraph describing the candidate's main strengths based on the resume.
    "improvements": a short paragraph suggesting specific improvements the candidate could make to their resume to better match the job description.
    "score": an integer representing the percentage match (0-100) between the resume and the job description.

    Resume Text:
    {resume_text}

    Job Description:
    {job_description_text}
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Check if the response is empty or a simple error message
        if not response.text:
            st.error("AI returned an empty response.")
            return None
        
        # Use a regex to find the JSON object and remove any extra text
        # This is a robust way to handle the model sometimes adding extra words
        # or backticks around the JSON.
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        
        if not json_match:
            st.error("Could not find a valid JSON object in the AI's response.")
            st.write(f"Raw response from AI: {response.text}")
            return None
            
        json_string = json_match.group(0)
        feedback = json.loads(json_string)
        return feedback
        
    except json.JSONDecodeError:
        st.error("AI did not return a valid JSON format. Check the model's raw output.")
        st.write(f"Raw response from AI: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error with Generative AI analysis: {e}")
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="Resume Feedback Analyzer")
st.title("Resume Feedback Analyzer")
st.markdown(
    """
    **Your personal AI mentor for job applications!**
    Upload your resume and a job description to get instant feedback on your skills.
    """
)

# File uploader for the resume
uploaded_resume = st.file_uploader(
    "Upload your Resume (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=False,
)

# Text area for the job description
job_description = st.text_area(
    "Paste the Job Description here:",
    height=300,
    help="Copy and paste the entire job description from the job posting.",
)

# Button to trigger the analysis
if st.button("Analyze Resume", type="primary"):
    if not uploaded_resume or not job_description:
        st.warning("Please upload a resume and paste a job description to start.")
    else:
        with st.spinner("Analyzing... this might take a moment."):
            file_extension = uploaded_resume.name.split('.')[-1].lower()
            if file_extension == 'pdf':
                resume_text = extract_text_from_pdf(uploaded_resume)
            elif file_extension == 'docx':
                resume_text = extract_text_from_docx(uploaded_resume)
            else:
                resume_text = ""

            if not resume_text:
                st.error("Could not extract text from the uploaded file.")
            else:
                feedback = analyze_resume_with_llm(resume_text, job_description)

                if feedback:
                    # Display the score
                    st.header("Resume Match Score")
                    st.metric(label="Overall Match", value=f"{feedback.get('score', 0)}%")
                    st.progress(int(feedback.get('score', 0)) / 100)
                    st.markdown("---")
                    
                    # Display the detailed feedback
                    st.header("Feedback Analysis")
                    
                    st.subheader("✅ Matched Skills")
                    if feedback.get('matched_skills'):
                        st.info(", ".join(feedback['matched_skills']))
                    else:
                        st.warning("No skills from the job description were matched.")

                    st.subheader("💡 Missing Skills")
                    if feedback.get('missing_skills'):
                        st.warning(", ".join(feedback['missing_skills']))
                    else:
                        st.success("You have all the key skills from the job description. Great job!")

                    st.subheader("⭐ Strengths")
                    st.write(feedback.get('strengths', ''))

                    st.subheader("🚀 Improvements")
                    st.write(feedback.get('improvements', ''))