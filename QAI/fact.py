import os
import openai
import tiktoken
from pdf import *
import math
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
def fact(questions):
    data_folder = "data"
    wav_files = [file for file in os.listdir(data_folder) if file.endswith(".txt")]
    i=1
    out=[]
    for wav_file in wav_files:
        file_path = os.path.join(data_folder, wav_file)
        with open(file_path, 'r') as file:
            text = file.read()
            y=get_completion("score the answer "+text+" based on the question "+questions[i-1]+" out of 5 only score is needed no explanation")
            out.append(y)
        i+=1
    out=list(map(int,out))
    return round(sum(out)/len(out))
# fact(['Tell me about yourself','What all projects did you work on at your internship','What was your role at the internship','What did you learn from your project on stock market prediction','How did you approach your project NoCodemML'])
