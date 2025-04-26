import json
import time
import os
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
time.sleep(2)
os.system('clear')

# Load intents
data = json.load(open("intents.json", 'r'))
load_prio = json.load(open("priorities.json","r"))
prior_intent = [values for values in load_prio["prior_intent"]]

def extract_ngrams(user):
    tokens = word_tokenize(user)
    tokens = [word for word in tokens if word not in string.punctuation]
    unigrams = tokens
    bigrams_ = [' '.join(b) for b in bigrams(tokens)]
    trigrams_ = [' '.join(t) for t in trigrams(tokens)]
    return unigrams + bigrams_ + trigrams_

def smart_intent(user_input):
    try:
        token = extract_ngrams(user_input)
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in token]
        print(lemmatized_words)

        intent_scores = {}

        for intent in data:
            max_score = max(fuzz.partial_ratio(keyword, " ".join(lemmatized_words)) for keyword in data[intent])            
            if max_score >= 75:  
                intent_scores[intent] = max_score
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_intents if sorted_intents else [('Unknown', 0)] 

    except Exception as e:
        return f'Error: {e}'

'''
def smart_intent(user,stopwords):
    try:
        token = extract_ngrams(user)
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in token]
        print(lemmatized_words)

        detect_intent = "Unknown"
        word_score = 0

        for intent in prior_intent:
            if intent in data:
                for keyword in data[intent]:
                    similarity = fuzz.partial_ratio(' '.join(lemmatized_words),keyword)
                    if similarity > word_score and similarity >= 80:
                        word_score = similarity
                        detect_intent = intent

        return detect_intent

    except Exception as e:
        return f'It Works?... {e}'
'''
# Test the function
while True:
    user_input = input("You: ")
    if user_input == "q":
        break
    intent = smart_intent(user_input)
    print(f"Intent: {intent}")
