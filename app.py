import streamlit as st
import PyPDF2
from docx import Document
import spacy
import io
import re

# Load the small English spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a list of common tech skills for keyword matching
# This is a simple but effective way to start
SKILLS_KEYWORDS = [
    'Python', 'Java', 'C++', 'JavaScript', 'React', 'Angular',
    'Vue.js', 'Node.js', 'HTML', 'CSS', 'SQL', 'NoSQL', 'MongoDB',
    'PostgreSQL', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
    'Git', 'GitHub', 'CI/CD', 'Agile', 'Scrum', 'Data Science',
    'Machine Learning', 'Deep Learning', 'PyTorch', 'TensorFlow',
    'Flask', 'Django', 'REST API'
]

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
        # Use io.BytesIO to handle the uploaded file
        doc = Document(io.BytesIO(uploaded_file.getvalue()))
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
    return text

# Function to analyze the resume against the job description
def analyze_resume(resume_text, job_description_text):
    # A simple, robust way to find skills is to check for their presence
    # in a case-insensitive manner.
    resume_skills = set()
    jd_skills = set()

    # Normalize both texts to lowercase for matching
    resume_lower = resume_text.lower()
    jd_lower = job_description_text.lower()

    # Find skills present in the resume
    for skill in SKILLS_KEYWORDS:
        if skill.lower() in resume_lower:
            resume_skills.add(skill)

    # Find skills present in the job description
    for skill in SKILLS_KEYWORDS:
        if skill.lower() in jd_lower:
            jd_skills.add(skill)

    # Determine matched, missing, and extra skills
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)
    extra_skills = resume_skills.difference(jd_skills)

    return matched_skills, missing_skills, extra_skills

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
            # Determine file type and extract text
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
                # Perform the analysis
                matched, missing, extra = analyze_resume(resume_text, job_description)

                # --- NEW CODE FOR STRETCH GOAL ---
                # Calculate the resume score
                total_skills_in_jd = len(matched) + len(missing)
                if total_skills_in_jd > 0:
                    score = (len(matched) / total_skills_in_jd) * 100
                else:
                    score = 0

                # Display the score using st.metric and a progress bar
                st.header("Resume Match Score")
                score_display = f"{score:.1f}%"
                st.metric(label="Overall Match", value=score_display)
                st.progress(int(score) / 100)
                st.markdown("---")
                # --- END OF NEW CODE ---

                # Display the results
                st.header("Feedback Analysis")
                st.markdown("---")

                # Matched skills (Strengths)
                st.subheader("Strengths (Matched Skills)")
                if matched:
                    st.success(f"**Found {len(matched)} skills from the job description in your resume:**")
                    st.info(", ".join(sorted(list(matched))))
                else:
                    st.warning("No matching skills were found. Try to tailor your resume to the job description.")

                # Missing skills (Areas for Improvement)
                st.subheader("Areas for Improvement")
                if missing:
                    st.warning(f"**You are missing {len(missing)} key skills from the job description:**")
                    st.markdown("Consider adding or highlighting these skills in your resume if you have experience with them.")
                    st.error(", ".join(sorted(list(missing))))
                else:
                    st.success("You have all the key skills from the job description. Great job!")

                # Additional skills (Improvements)
                st.subheader("Additional Skills")
                if extra:
                    st.info(f"**Your resume also lists the following skills not in the job description:**")
                    st.markdown("These could be valuable additions to showcase your breadth of knowledge.")
                    st.success(", ".join(sorted(list(extra))))
