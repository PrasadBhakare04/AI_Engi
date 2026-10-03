from parser_functions import parse_resume, ask_question
from pathlib import Path
import json

resume_path = "E:/Programming/AI/_1SelfMade/week2_day5-project-Personal-ChatBot/resume/resume1.pdf"
print(parse_resume(Path(resume_path)).model_dump_json(indent = 2))

ask_question("what are his skills only give me skills don't add filler lines")

ask_question("can i hire him for a web developer role ?")