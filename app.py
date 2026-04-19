import os
import PyPDF2  # Added import here
from flask import Flask, render_template, request, redirect, url_for
from ml_model import extract_skills_from_resume, suggest_additional_skills, generate_multilingual_roadmap

app = Flask(__name__)

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return text

@app.route('/')
def index():
    # Removed K_SERVICE and K_REVISION as they don't exist on Render
    return render_template('index.html', message="KaushalX is Live!")

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Check if the post request has the file part
        resume = request.files.get('resume')
        
        if resume and resume.filename != '':
            resume_text = extract_text_from_pdf(resume)
            
            if resume_text:
                # 1. Extract current skills
                extracted_skills_raw = extract_skills_from_resume(resume_text)
                
                # Convert string response to list (assuming Groq returns a list-like string)
                # This depends on your format_skills function in ml_model.py
                from ml_model import format_skills
                extracted_skills = format_skills(extracted_skills_raw)
                
                # 2. Get suggestions
                suggested_skills = suggest_additional_skills(extracted_skills)
                
                # 3. Generate Roadmap (Modified to use the first extracted skill dynamically)
                target_skill = extracted_skills[0] if extracted_skills else "Data Science"
                roadmap = generate_multilingual_roadmap(target_skill, "English")
                
                return render_template('dashboard.html', 
                                     extracted_skills=extracted_skills, 
                                     suggested_skills=suggested_skills, 
                                     roadmap=roadmap)
            else:
                return "Error: Could not read the PDF file.", 400
        else:
            return "Error: No resume file uploaded.", 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Render provides the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    # In production, Render uses gunicorn, but this is kept for local testing
    app.run(host='0.0.0.0', port=port)
