import os
import re
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return text

def extract_skills_from_resume(resume_text):
    prompt = f"""
    Extract only technical and soft skills related to software development, data science, and cloud computing from the following resume text.
    Do not include any extra words, just return a list of skills.

    Resume Text:
    {resume_text}

    Output format:
    - Skill 1
    - Skill 2
    - Skill 3
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except google.generativeai.types.generation_types.BlockedPromptException as e:
        return f"Error: The prompt was blocked: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def format_skills(skills_text):
    skills = []
    for line in skills_text.split("\n"):
        skill = line.strip("- ").strip()  # Remove leading/trailing spaces and hyphens
        if skill:  # Check if the line is not empty
            skills.append(skill)
    return skills

def suggest_additional_skills(existing_skills):
    prompt = f"""
    Based on the following skills, suggest a comprehensive list of additional skills 
    (20-30) that are highly valuable in the job market. Focus on:
    - Related technical skills
    - Current industry trends
    - In-demand tools and frameworks
    - Complementary soft skills
    - Emerging technologies

    Existing Skills:
    {', '.join(existing_skills)}

    Format the response only as a list (each skill prefixed with "- "). Do not provide explanations or categories.
    """

    try:
        response = model.generate_content([prompt])

        if response and hasattr(response, "text"):
            # ✅ Clean and parse the response to extract skills
            lines = response.text.split("\n")
            suggested_skills_list = []
            for line in lines:
                line = line.strip()
                if line.startswith("- "):
                    skill = line[2:].strip()
                    if skill and skill not in existing_skills:
                        suggested_skills_list.append(skill)

            # ✅ Remove duplicates
            suggested_skills_list = list(dict.fromkeys(suggested_skills_list))
            return suggested_skills_list

        return ["Error: No response from model."]
    except google.generativeai.types.generation_types.BlockedPromptException as e:
        return [f"Error: The prompt was blocked: {str(e)}"]
    except Exception as e:
        return [f"An unexpected error occurred: {str(e)}"]

def get_top_3_in_demand_skills():
    prompt = """
    Identify the top 3 most in-demand skills in the global job market.
    Focus on skills that offer high growth potential, are sought after by employers across industries, 
    and are useful in a wide range of roles.

    Format:
    - Skill 1
    - Skill 2
    - Skill 3

    Do NOT include any explanations.
    """

    try:
        response = model.generate_content([prompt])

        if response and hasattr(response, "text"):
            # ✅ Extract and clean top 3 skills
            lines = response.text.split("\n")
            top_skills = []
            for line in lines:
                line = line.strip()
                if line.startswith("- "):
                    skill = line[2:].strip()
                    if skill:
                        top_skills.append(skill)

            return top_skills[:3]  # Just to be safe, limit to top 3

        return ["Error: No response from model."]
    except google.generativeai.types.generation_types.BlockedPromptException as e:
        return [f"Error: The prompt was blocked: {str(e)}"]
    except Exception as e:
        return [f"An unexpected error occurred: {str(e)}"]

def generate_multilingual_roadmap(skill, language):
    prompt = f"""
    Create a complete and structured learning roadmap for the skill: "{skill}".

    Respond in: {language}

    Requirements:
    1. Roadmap should be beginner-friendly and advance gradually.
    2. For each topic, include:
        - Topic name
        - A short description (optional)
        - 1–2 YouTube video links (working links only)
        - 1–2 useful website links (tutorials, documentation, or courses from reputable online learning platforms)

    Use clean formatting:

    Topic: <topic name>
    Description: <one-liner>
    YouTube Links:
    - <youtube_link_1>
    - <youtube_link_2>
    Website Links:
    - <website_link_1>
    - <website_link_2>

    Only include real links that are currently working and relevant. Avoid unnecessary explanation.
    """

    try:
        response = model.generate_content([prompt])
        if response and hasattr(response, "text"):
            return response.text
        return "❌ No response from Gemini."
    except google.generativeai.types.generation_types.BlockedPromptException as e:
        return f"Error: The prompt was blocked: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
