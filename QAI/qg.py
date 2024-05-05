import os
import openai
import tiktoken
from pdf import *
# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = "key"
#openai.api_key  = os.environ['OPENAI_API_KEY']
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output 
    )
    return response.choices[0].message["content"]
def get_questions(file,x):
    text=read_pdf(file)
    # response = get_completion("Based on the resume given below create "+str(x) +" questions.\n"+text)
    response = get_completion("Based on the resume given below create "+str(x) +" questions both technical and project based.\n"+text)
    print(response)
    questions1=[response.split('\n')[i] for i in range(x)]
    questions=[]
    for i in questions1:
        questions.append(i[2:])
    print(questions)
    return questions
# get_questions('Joel_resume.pdf',4)