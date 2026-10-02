from parser_functions import parse_resume
from pathlib import Path
import json

resume_path = "E:/Programming/AI/_1SelfMade/week2_day5-project-Personal-ChatBot/resume/resume1.pdf"
print(parse_resume(Path(resume_path)).model_dump_json(indent = 2))