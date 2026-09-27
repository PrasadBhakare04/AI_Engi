import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re
from tools import calculator, get_product_price, tools_desc
import json

load_dotenv()
my_api_key=os.getenv("groq_api")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"


tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)
IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17")

Never write:
calculator(expression="5000 - 1000")
Follow these rules:

use the tools mentioned above
1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    isFinal = ""
    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools_desc,
            temperature=0
        )

        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            print(response.choices[0].message.content)
            break

        print(tool_calls)
        for tool_call in tool_calls : 
            function_name = tool_call.function.name
            function_to_call = tools[function_name]
            args_json = json.loads(tool_call.function.arguments)
            observation = function_to_call(**args_json)
            print(f"  -> Called {function_name}({args_json}) = {observation}")   

        messages.append({
            "role":"assistant",
            "content" : str(tool_calls)
        })

        messages.append({
            "role":"user",
            "content" : f"Observation {observation}"
        })
        sleep(5)



prompt="""
I have 5000 rupees. What is the price of an iphone 17?
and how much money will I have left?
"""

run_agent(prompt)