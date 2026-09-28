import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()

my_api_key = os.getenv("groq_api")

if not my_api_key:
    raise ValueError("Api key not found")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-20b"

JD = """
We are hiring a Backend Python Developer.
Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIS
- 2+ years of experience
"""

RESUME = """
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt, user_prompt):
    sys_message = {
        "role":"system",
        "content":system_prompt
    }

    user_message = {
        "role" : "user",
        "content" : user_prompt
    }

    messages = [sys_message, user_message]

    answer = client.chat.completions.create(model=model, messages = messages).choices[0].message.content

    return answer

def step1_res_extract():
    sys_prompt = """
        You are a professional HR assistant. Extract the name, contact if any and skills from the candidate resumse provided.
        Only return the skills no other information. Do not invent any skills by yourself
        output format should be
        name:
        skills:
    """

    user_prompt = f"""
        Extract the skills from the resume
        {RESUME}
    """

    return ask_llm(sys_prompt, user_prompt)

def step2_jd_extract():
    sleep(5)
    sys_prompt = """
        You are a professional HR assistant. Extract the skills from the job description provided.
        Only return the skills no other information. Do not invent any skills by yourself
    """

    user_prompt = f"""
        Extract the skills from the job description
        {JD}
    """

    return ask_llm(sys_prompt, user_prompt)

def step3_match(candidate, jd):
    sys_prompt = """
                You are a professional HR assistant. from the job skills and candidate skills i will provide compare them and give the score according to that.
                If the score is greater than 60 then the candidate is good for the role.
                and produce a short verdict why you gave the score.
                If candidate has any additional skills which is used widely in every technology or role for e.g git, while scoring consider that also
                the output format should be
                candidate name:
                matching skills:
                score:
                verdict:
            """

    user_prompt = f"""
            Here is the job description skills and resume skills compare them and tell me if the candidate is fit for the role or not ?
            candidate : {candidate}
            job description : {jd}
        """

    return ask_llm(sys_prompt, user_prompt)

print(step3_match(step1_res_extract(), step2_jd_extract()))

