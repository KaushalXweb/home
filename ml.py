import os
import PyPDF2
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Using Llama-3.3-70b for high reasoning quality, similar to Gemini Pro
MODEL_NAME = "llama-3.3-70b-versatile"

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

def get_groq_response(prompt):
    """Helper function to handle Groq API calls"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_NAME,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

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
    return get_groq_response(prompt)

def format_skills(skills_text):
    skills = []
    for line in skills_text.split("\n"):
        skill = line.strip("- ").strip()
        if skill:
            skills.append(skill)
    return skills

def suggest_additional_skills(existing_skills):
    prompt = f"""
    Based on the following skills, suggest a comprehensive list of additional skills (20-30) that are highly valuable in the job market. Focus on:
    - Related technical skills
    - Current industry trends
    - In-demand tools and frameworks
    - Complementary soft skills
    - Emerging technologies

    Existing Skills:
    {', '.join(existing_skills) if isinstance(existing_skills, list) else existing_skills}

    Format the response only as a list (each skill prefixed with "- "). Do not provide explanations or categories.
    """
    
    response_text = get_groq_response(prompt)
    
    if "Error:" in response_text:
        return [response_text]

    lines = response_text.split("\n")
    suggested_skills_list = []
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            skill = line[2:].strip()
            if skill:
                suggested_skills_list.append(skill)

    return list(dict.fromkeys(suggested_skills_list))

def get_top_3_in_demand_skills():
    prompt = """
    Identify the top 3 most in-demand skills in the global job market.
    Format:
    - Skill 1
    - Skill 2
    - Skill 3
    Do NOT include any explanations.
    """
    response_text = get_groq_response(prompt)
    
    if "Error:" in response_text:
        return [response_text]

    lines = response_text.split("\n")
    top_skills = [line[2:].strip() for line in lines if line.strip().startswith("- ")]
    return top_skills[:3]

def generate_multilingual_roadmap(skill, language):
    prompt = f"""
    Create a complete and structured learning roadmap for the skill: "{skill}".
    Respond in: {language}

    Requirements:
    1. Roadmap should be beginner-friendly.
    2. For each topic, include:
        - Topic: <topic name>
        - Description: <one-liner>
        - YouTube Links: - <link>
        - Website Links: - <link>

    Only include real links. Avoid unnecessary explanation.
    """
    return get_groq_response(prompt)
