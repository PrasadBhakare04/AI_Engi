# Approach is that convert all the resumes into text and pass them with the userpropmt in a loop for each resume separately. The job description and the schema is in the system prompt #

from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path
import os
from pypdf import PdfReader

load_dotenv()
my_api_key = os. getenv("groq_api")

#create client 
client = Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

class Candidate(BaseModel):
    name:str
    score:int
    skills:list
    email:str

schema = Candidate.model_json_schema()

system_prompt=f"""
this is the job description
Company: CloudByte Technologies
Job Title: Full Stack Developer
Location: Bengaluru, India
Experience: 1–3 years

Job Description:

CloudByte Technologies is hiring a Full Stack Developer to build scalable and responsive web applications.

Responsibilities:
- Develop responsive frontend applications using React.js.
- Build backend services using Node.js and Express.js.
- Develop and consume REST APIs.
- Design database schemas using MongoDB and PostgreSQL.
- Implement authentication and authorization using JWT.
- Integrate third-party APIs.
- Write unit and integration tests.
- Debug and optimize application performance.
- Deploy applications using Docker and cloud platforms.
- Work closely with product managers and UI/UX designers.

Required Skills:
- JavaScript
- TypeScript
- React.js
- Node.js
- Express.js
- MongoDB
- PostgreSQL
- REST API
- HTML5
- CSS3
- Git
- GitHub

Preferred Skills:
- Next.js
- Redux
- Docker
- AWS
- Redis
- Jest
- CI/CD
- Agile/Scrum

Education:
- Bachelor's degree in Computer Science, IT, or equivalent.

the response format strictly should be json 
{schema}
"""
system_message={
    "role":"system",
    "content": system_prompt
}

#Reading the pdf and converting into text
#----------------------------------------------------------------#

resume_folder = Path("resumes")

for pdf_file in resume_folder.glob("*.pdf"):
    reader = PdfReader(pdf_file)
    resume_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    user_prompt=f"""from the text of the resume extract the information and give scores based on the job description. Score it out of hundred and also give me their name, score, email and skills(list) {resume_text}"""
    message = {
        "role":"user",
        "content":user_prompt
    }

    messages = [system_message, message]

    
    response = client.chat.completions.create(model=model, messages=messages)

    print(response.choices[0].message.content)
#----------------------------------------------------------------#
# pdf_path = "resume1.pdf"

# # Read PDF
# reader = PdfReader(pdf_path)

# resume_text = ""

# for page in reader.pages:
#     text = page.extract_text()

#     if text:
#         resume_text += text + "\n"
