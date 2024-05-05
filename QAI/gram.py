# pip install -U git+https://github.com/PrithivirajDamodaran/Gramformer.git
# python -m spacy download en_core_web_sm
from math import ceil
from gramformer import Gramformer
import torch
import re
import os

def calc_score(num,len):
  len=len/5
  score= 1-(num/(len))
  print("score",score)
  if 0.9 < score <= 1:
    return 5
  elif 0.7 < score <= 0.9:
    return 4
  elif 0.4 < score <= 0.7:
    return 3
  elif 0.2 < score <= 0.4:
    return 2
  else:
    return 1

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
def gram_fun(sentence):
  set_seed(1212)

  gf = Gramformer(models = 1, use_gpu=True) # 1=corrector, 2=detector
  # sentence = "Me and my friends is goes to the park yesterday and buyed ice creams but she don't likes it because it's too cold and we has not enough money for buy more."
  pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
  influent_sentences = re.split(pattern, sentence)
  error=0
  for influent_sentence in influent_sentences:
      corrected_sentences = gf.correct(influent_sentence, max_candidates=1)
      print("[Input] ", influent_sentence)
      for corrected_sentence in corrected_sentences:
      #   print("[Edits] ", gf.get_edits(influent_sentence, corrected_sentence))
        # error+=(len(gf.get_edits(influent_sentence, corrected_sentence)))
        for e in gf.get_edits(influent_sentence, corrected_sentence):
          print(e)
          error+=1
          # if("SVA" in e[0]):
          #   error+=0.4
          # elif("TENSE" in e[0]):
          #   error+=0.4
          # elif("FORM" in e[0]):
          #   error+=0.25
          # elif("VERB" in e[0]):
          #   error+=0.3
          # elif("DET" in e[0]):
          #   error+=0.25
          # elif("PREP" in e[0]):
          #   error+=0.25
          # elif("PRON" in e[0]):
          #   error+=0.25
          # elif("SPELL" in e[0]):
          #   error+=0
          # else:
          #   error+=0.15
      print("-" *100)
  print(error)
  return calc_score(error,len(sentence.split()))
def grammar():
    data_folder = "data"
    wav_files = [file for file in os.listdir(data_folder) if file.endswith(".txt")]
    i=1
    out=[]
    for wav_file in wav_files:
        file_path = os.path.join(data_folder, wav_file)
        with open(file_path, 'r') as file:
            text = file.read()
            y=gram_fun(text)
            out.append(y)
    print('average',round(sum(out)/len(out)))
    return round(sum(out)/len(out))
# grammar()
