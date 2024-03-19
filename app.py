from dotenv import load_dotenv

load_dotenv()

import streamlit as st 
import os, io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None : 
        ## Convert the PDF to Image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        #Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode()    #encode to base 64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Streamlit App
    
st.set_page_config(page_title = "ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description : ", key = "input")

uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me About the Resume")

# submit2 = st.button("How can I Improvise My Skills")

# submit3 = st.button("Missing Keywords")

submit2 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in AIML, Data Science, Natural language processing, Data Analyst, Deep learning, Generative AI, LLM. 
Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with this role.
Hifhlight the strength and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 ="""
You are an akilled ATS (Application Tecking System) scanner with a deep understanding of AIML, Data Science, Natural language processing, Data Analyst, Deep learning, Generative AI, LLM,
and deep ATS functionality.
Your task is to review the provided resume against the  provided job description and give the Percentage of match if the resume matches 
job description. 
First the output should come up as Percentage match and then keywords missing in resume as per the job requirements.

"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is :")
        st.write(response)
    else:
        st.write("Please upload the resume")
