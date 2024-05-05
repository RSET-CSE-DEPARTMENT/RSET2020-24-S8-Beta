from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import os
from collections import Counter
def sentanalysis(text):
    def preprocess(text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return scores,ranking
    # for i in range(scores.shape[0]):
    #     l = config.id2label[ranking[i]]
    #     s = scores[ranking[i]]
    #     print(f"{i+1}) {l} {np.round(float(s), 4)}")
def sentiment_analysis():
    data_folder = "data"
    wav_files = [file for file in os.listdir(data_folder) if file.endswith(".txt")]
    i=1
    out=[]
    for wav_file in wav_files:
        file_path = os.path.join(data_folder, wav_file)
        with open(file_path, 'r') as file:
            text = file.read()
            x,y=sentanalysis(text)
            out.append(y[0])
    out=Counter(out)
    most_common_element = out.most_common(1)[0][0]
    if(most_common_element==0):
        print("Negative")
    elif(most_common_element==1):
        print("Neutral")
    else:
        print("Positive")
    return most_common_element
# sentiment_analysis()
# sentiment_analysis("I am so happy")