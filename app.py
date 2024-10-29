from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Index Page
@app.route('/')
def index():
    return render_template('index.html')

# Results Page
@app.route('/customize', methods=['POST'])
def customize_resume():
    # Get user inputs from the form
    resume = request.form['resume']
    job_description = request.form['job_description']
    
    # Initialize OpenAI API
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    # Prompt
    prompt = (
        f"Here is a resume:\n{resume}\n\n"
        f"And here is a job description:\n{job_description}\n\n"
        "Tailor my resume according to above given Job description and write in easy professional English don't use AI words."
        "Make the resume ATS-friendly."
        "Don't skip jobs from resume."
        "Highlight the changes that you have done in resume."
        "Use proper HTML tags for formatting, such as <strong> for bold text and <p> for paragraphs."
    )

    # OpenAI GPT-40
    response = openai.chat.completions.create(
        model="gpt-4o", 
        messages= [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                }
            ]
            }
        ]
    )

    # Extract the response
    response_content = response.choices[0].message.content

    # Return response to Results page
    return render_template('result.html', customized_resume=response_content)

if __name__ == "__main__":
    app.run(debug=True)
