import openai
import os
from django.conf import settings

GPT_API_Key = 'sk-proj-ONpJm8U98WCNI7svpM2jT3BlbkFJPHMMw0BNarVHyYRIRojA'
# openai_api_key = os.environ.get('GPT_API_Key')
openai.api_key = GPT_API_Key

# List of keywords related to medicines and health topics
medicine_keywords = ['medicine', 'treatment', 'hospital', 'health', 'symptoms', 'diagnosis', 'prescription', 'doctor', 'patient']

def is_medicine_related(message):
    # Check if the message contains any medicine-related keywords
    for keyword in medicine_keywords:
        if keyword in message.lower():
            return True
    return False

def ask_openai(message):

    if not is_medicine_related(message):
        return "Sorry, I can only answer questions related to medicines and health topics."
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer
