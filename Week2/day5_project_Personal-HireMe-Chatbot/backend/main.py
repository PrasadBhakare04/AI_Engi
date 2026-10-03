from fastapi import FastAPI
from util import read_resume, parse_resume
from pathlib import Path


app = FastAPI()

@app.get("/")
def home():
    text = read_resume(Path("resume1.pdf"))
    resume = parse_resume(text)
    print(resume.model_dump_json(indent=2))
    return {
        "message" : "resume parsed"
    }