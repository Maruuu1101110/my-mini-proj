import json
import time
import os
import re
import string
import nltk
from nltk.util import bigrams,trigrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rapidfuzz import fuzz

#Download missing deps
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

print("Finished Downloading...")
os.system('cls')

script_dir = os.path.dirname(__file__)
intents_path = os.path.join(script_dir, "intents.json")
priorities_path = os.path.join(script_dir, "priorities.json")

# Load intents
data = json.load(open(intents_path, "r", encoding="utf-8"))
load_prio = json.load(open(priorities_path, "r", encoding="utf-8"))
prior_intent = [values for values in load_prio["prior_intent"]]

def extract_ngrams(user):
    tokens = word_tokenize(user)
    tokens = [word for word in tokens if word not in string.punctuation]
    unigrams = tokens
    bigrams_ = [' '.join(b) for b in bigrams(tokens)]
    trigrams_ = [' '.join(t) for t in trigrams(tokens)]
    return unigrams + bigrams_ + trigrams_


def segment_sentences(text):
    # Properly split using conjunctions and punctuation, escaping special characters
    segments = re.split(r'\b(?:and|then)\b|[,.?]', text, flags=re.IGNORECASE)
    segments = [segment.strip() for segment in segments if segment.strip()]
    return segments

def smart_intent(user, data=None, threshold=75): 
    try: 
        if data is None:
            with open(intents_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        segments = segment_sentences(user) 
        detected_intents = []

        for segment in segments:
            token = segment.split()
            detect_intent = "Unknown"
            best_score = 0
        
            for intent, keywords in data.items():
                scores = [fuzz.partial_ratio(keyword, segment) for keyword in keywords]
                max_score = max(scores, default=0)
            
                if max_score > threshold and max_score > best_score:
                    detect_intent = intent
                    best_score = max_score
        
            detected_intents.append((detect_intent, best_score))
    
        return detected_intents

    except Exception as e:
        return f'Error: {e}'
    

if __name__=="__main__":
    while True:
        user_input = input("You: ")
        if user_input == "q":
            break
        intent = smart_intent(user_input, data)
        print(f"Intent: {intent}")