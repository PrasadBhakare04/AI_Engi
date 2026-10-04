from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from util import read_resume, parse_resume, ask_candidate, ChatRequest, get_resume
from pathlib import Path
from time import sleep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your site's URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    resume = get_resume()
    print(resume.model_dump_json(indent=2))
    return {
        "message" : "resume parsed"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    resume = get_resume()

    stream = ask_candidate(
        request.question,
        resume
    )

    def generate():

        for chunk in stream:

            content = chunk.choices[0].delta.content

            if content:
                yield content
                sleep(0.05)

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )