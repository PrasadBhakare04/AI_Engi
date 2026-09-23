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

    user_prompt=f"""from the text of the resume extract the information and give scores based on the skills relevance to the required skills i am mentioning the skills required are java, python, mernstack. Score it out of hundred and also give me their name, score, email and skills(list) {resume_text}"""
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
