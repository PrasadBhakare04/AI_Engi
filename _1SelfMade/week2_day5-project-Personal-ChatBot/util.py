from groq import Groq
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from pathlib import Path

load_dotenv()

my_api_key = os.getenv("groq_api")
client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-20b"

class Experience(BaseModel) :
    company_name: str
    role : str
    skills_used : list[str]
    start_date : str
    end_date: str
    duration : int

class Resume(BaseModel):
    name : str | None = None
    short_description : str | None = None
    skills : list[str] | None
    certifications : list[str] | None
    experience : list[Experience] | None
    phone : int | None = None
    email : str | None = None
    education : list[str] | None
    projects : list[str] | None

resume_schema = Resume.model_json_schema()

class JobDescription(BaseModel):
    role : str
    responsibilities : list[str]
    required_skills : list[str]
    optional_skills : list[str]
    required_experience_years : int
    educational_requirements : list[str]