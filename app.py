import os
import requests
from flask import Flask, request
import openai


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
    
# Endpoint to handle incoming messages from WhatsApp
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract the message content from the incoming request
    message = data['messages'][0]['body']

    # Call the ChatGPT API to process the message
    response = chat_with_gpt(message)

    # Send the response back to WhatsApp
    send_message(response)

    return 'Message sent'

def chat_with_gpt(message):
    # Call the ChatGPT API to generate a response
    gpt_response = requests.post(
        'https://api.openai.com/v1/engines/davinci-codex/completions',
        headers={
            'Authorization': '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',
            'Content-Type': 'application/json'
        },
        json={
            'prompt': message,
            'max_tokens': 50
        }
    )

    # Extract the generated response from the API response
    response = gpt_response.json()['choices'][0]['text']

    return response

def send_message(message):
    # Use TMWhatsApp to send the message to WhatsApp
    # Replace 'TO_NUMBER' with the phone number to send the message to
    to_number = '0740458874'

    # Replace 'FROM_NUMBER' with your registered TMWhatsApp number
    from_number = '0740458874'

    # Log in to TMWhatsApp
    whatsapp.login()

    # Send the message
    whatsapp.send_message(to_number, message)

    # Log out from TMWhatsApp
    whatsapp.logout()

if __name__ == '__main__':
    app.run()

