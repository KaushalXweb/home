"""
A sample Hello World server.
"""
import os
from ml_model import extract_skills_from_resume, suggest_additional_skills, generate_multilingual_roadmap
from flask import Flask, render_template, request, redirect, url_for

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        skills = request.form.get('skills')
        resume = request.files.get('resume')

        if resume:
            resume_text = extract_text_from_pdf(resume)
            if resume_text:
                extracted_skills = extract_skills_from_resume(resume_text)
                suggested_skills = suggest_additional_skills(extracted_skills)
                roadmap = generate_multilingual_roadmap("Data Science","English")
                print("Extracted Skills:", extracted_skills)
                print("Suggested Skills:", suggested_skills)
                print("Roadmap:\n", roadmap)
                return render_template('dashboard.html', extracted_skills=extracted_skills, suggested_skills=suggested_skills, roadmap=roadmap)
            else:
                return "Error extracting text from PDF", 500
        else:
            print("Skills:", skills)
            return redirect(url_for('dashboard'))

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
