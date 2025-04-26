import nltk
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
print(stopwords)

from rapidfuzz import fuzz
from nltk.stem import WordNetLemmatizer

def smart_intent(user, stopwords):
    try:
        # Tokenization and lemmatization
        token = extract_ngrams(user)  # Assuming extract_ngrams is your custom tokenizer
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in token]
        print(lemmatized_words)

        detect_intent = 'Unknown'
        best_score = 0

        for intent in prior_intent:
            if intent in data:
                for keyword in data[intent]:
                    similarity = fuzz.ratio(' '.join(lemmatized_words), keyword)  # Compare entire user input
                    if similarity > best_score and similarity >= 70:  # 80% threshold
                        best_score = similarity
                        detect_intent = intent

        return detect_intent

    except Exception as e:
        return f'Error: {e}'

def smart_intent(user_input):
    try:
        token = extract_ngrams(user_input)
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in token]
        print(lemmatized_words)

        intent_scores = {}

        for intent in data:  # Loop through all intents
            max_score = max(fuzz.partial_ratio(keyword, " ".join(lemmatized_words)) for keyword in data[intent])
            
            if max_score >= 70:  # Only consider intents with a score above 70%
                intent_scores[intent] = max_score

        # Sort intents by their confidence score (highest first)
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_intents if sorted_intents else [('Unknown', 0)]  # Return list of intents

    except Exception as e:
        return f'Error: {e}'


import re from rapidfuzz import fuzz

def segment_sentences(text): # Split using common conjunctions and punctuation 
    segments = re.split(r'\band\b|\bthen\b|,|.|?', text, flags=re.IGNORECASE) 
    segments = [segment.strip() for segment in segments if segment.strip()] 
    return segments

def smart_intent(user, data, threshold=75): 
    try: 
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

#Example data structure for intents

data = { "reminder": ["remind me", "set a reminder", "remember to"], "weather": ["weather", "forecast", "temperature"], "casual_chat": ["how are you", "what's up", "hello"], }

Example usage

user_input = "Remind me to call mom later and check the weather." 
print(smart_intent(user_input, data))


