# Importing the required libraries

from flask import request,jsonify

from flask import Flask 

from dotenv import load_dotenv

# from openai import OpenAI

# FinancialBERT
from transformers import pipeline

# Loading the environment variables
load_dotenv('config/.env')

# Creating the Flask app
app = Flask(__name__)


# FinancialBERT
model = pipeline('text-generation' , model='microsoft/DialoGPT-small')

# Creating the OpenAI client
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Defining the route for the chatbot
@app.route('/chat', methods=['POST'])
def chat():

    # Getting the data
    data = request.json

    try : 
        # Creating the conversation
        response = model(data['messages'][-1]['content'] , max_length=50 , num_return_sequences=1, pad_token_id = 50256)

        # Getting the response
        # response = model(conv)

        # Getting the generated text
        generated = response[0]['generated_text']

        # Getting the input text
        input_text = data['messages'][-1]['content']

        # Getting the message
        if generated.startswith(input_text):
            message = generated[len(input_text):].strip()
        else:
            message = generated

        # Returning the response
        return jsonify({"message": message})
    except Exception as e:

        # Returning the error
        return jsonify({
            "error" : str(e) 
        })


# Running the app
if __name__ == "__main__":
         app.run(debug=True)