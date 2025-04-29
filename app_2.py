import streamlit as st
from docx import Document
from openai import OpenAI

import os
from datetime import datetime

client = OpenAI(api_key=st.secrets["openai_key"])


def fill_template(template_path, output_path, replacements):
    doc = Document(template_path)
    for para in doc.paragraphs:
        for key, value in replacements.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, value)
    doc.save(output_path)

st.title("AI-Powered JD Generator")

with st.form("jd_form"):
    role = st.text_input("Role", "Power BI Developer")
    experience = st.text_input("Experience", "5 years")
    location = st.text_input("Location", "Bangalore")
    reporting_to = st.text_input("Reporting To", "Head of Analytics")
    must_skills = st.text_area("Required Skills", "Power BI, DAX, SQL")
    optional_skills = st.text_area("Secondary Skills", "Excel, Power Automate")
    org_support = st.text_area("Organizational Support", "Supported by data team")
    roadmap = st.text_area("Future Roadmap", "Opportunity to lead analytics")
    qualifications = st.text_area("Qualifications", "B.Tech / MCA with 5 years exp.")
    inclusion = st.text_area("Inclusion Statement", "We are an equal opportunity employer.")

    submitted = st.form_submit_button("Generate JD")

if submitted:
    with st.spinner("Generating JD with AI..."):
        prompt = f"""
Write a professional JD for:
Role: {role}
Experience: {experience}
Location: {location}
Reporting To: {reporting_to}
Required Skills: {must_skills}
Optional Skills: {optional_skills}
Organizational Support: {org_support}
Future Roadmap: {roadmap}
Qualifications: {qualifications}
Inclusion Statement: {inclusion}
"""
    
        response = client.chat.completions.create(
           model="gpt-3.5-turbo",
           messages=[{"role": "user", "content": prompt}]
        )
        jd_text = response.choices[0].message.content


        replacements = {
            "Job Description": jd_text,
            "AboutTheJob": "This role involves creating reports and insights.",
            "Role": role,
            "Location": location,
            "ReportingTo": reporting_to,
            "Responsibilities": "• Build dashboards\n• Manage stakeholders\n• Ensure data quality",
            "RequiredSkills": must_skills,
            "OptionalSkills": optional_skills,
            "OrganizationalSupport": org_support,
            "FutureRoadmap": roadmap,
            "Qualifications": qualifications,
            "InclusionStatement": inclusion,
        }

        template_path ="C:\\Users\\malavika.v\\Desktop\\JD-Generator\\templates\\JD.docx"
        filename = f"JD_{role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
        output_path = f"generated/{filename}"
        fill_template(template_path, output_path, replacements)

        st.success("JD generated successfully!")
        with open(output_path, "rb") as f:
            st.download_button("Download JD", f, file_name=filename)
