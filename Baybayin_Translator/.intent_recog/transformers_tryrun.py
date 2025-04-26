from transformers import pipeline

generator = pipeline("text-generation", model="microsoft/DialoGPT-small")

response = generator("Hello, how are you?", max_length=50)
print(response[0]['generated_text'])
