from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Function to interact with ChatGPT
def chat_with_gpt(prompt):
    try:
        # Send the prompt to ChatGPT and get the response
        completion = client.completions.create(prompt=prompt, model='gpt-3.5-turbo-0125', max_tokens=100)

        # Return the generated response
        return completion.choices[0].text.strip()

    except Exception as e:
        print("Error:", str(e))
        return "Sorry, I encountered an error while processing your request. Error details: " + str(e)



        
# Function to handle user queries
def handle_query(query):
    # Check if the query is related to medicine
    if 'medicine' in query.lower() or 'drug' in query.lower():
        # Call ChatGPT with the user query
        response = chat_with_gpt(query)

        # Return the response from ChatGPT
        return response
    else:
        # Return a generic response for queries outside of medicine
        return "Sorry, I don't know!!"


