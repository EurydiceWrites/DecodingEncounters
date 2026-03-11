import streamlit as st
import json
import time
import pandas as pd
import pdfplumber
import io
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🚀 Local AI Resume Screener")
st.markdown("Drop your 800 PDFs below. Gemini Flash will analyze them locally and spit out a ranked Excel sheet.")

prompt = """You are an expert technical recruiter analyzing a resume.
Extract the applicant's key qualifications and output EXACTLY a JSON dictionary.
The 'Pass_Screening' boolean should evaluate to true ONLY if they have either 3+ years of experience OR a Bachelor's Degree.

{
  "Filename": "File Name",
  "Name": "Applicant Name",
  "Years_Experience": 5,
  "Has_Degree": true,
  "Top_3_Skills": ["Python", "AWS", "SQL"],
  "Pass_Screening": true,
  "Reason": "Brief reason for pass/fail based on 3+ years or degree requirement."
}

RESUME TEXT:
"""

uploaded_files = st.file_uploader("Upload PDF Resumes", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("Start Batch Screening"):
        results = []
        progress_bar = st.progress(0)
        status = st.empty()
        
        for i, file in enumerate(uploaded_files):
            status.text(f"Scanning: {file.name} ({i+1}/{len(uploaded_files)})")
            try:
                raw_text = ""
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            raw_text += text + "\n"
                            
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt + raw_text,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.0
                    )
                )
                
                data = json.loads(response.text)
                data['Filename'] = file.name
                results.append(data)
                
                time.sleep(1) # Rate limit protection
                
            except Exception as e:
                st.error(f"Error on {file.name}: {e}")
                
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        status.text("Screening Complete!")
        st.success(f"Successfully screened {len(results)} resumes!")
        
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df.style.applymap(lambda x: 'background-color: lightgreen' if x is True else ('background-color: lightcoral' if x is False else ''), subset=['Pass_Screening']))
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name='resume_screening_results.csv',
                mime='text/csv',
            )
