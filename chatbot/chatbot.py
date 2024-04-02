import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key'

# Function to interact with ChatGPT
def chat_with_gpt(prompt):
    try:
        # Send the prompt to ChatGPT and get the response
        response = openai.Completion.create(
            engine="davinci",  # Choose the GPT model
            prompt=prompt,
            max_tokens=100
        )

        # Return the generated response
        return response.choices[0].text.strip()

    except Exception as e:
        print("Error:", str(e))
        return "Sorry, I encountered an error while processing your request."


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


