import os
import requests
from flask import Flask, request

app = Flask(__name__)

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
            'Authorization': 'Bearer YOUR_API_KEY',
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
    # Code to send the message back to WhatsApp using the WhatsApp API
    # Replace this with your own implementation

    # Example using Twilio API
    from twilio.rest import Client

    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    # Replace 'TO_NUMBER' with the phone number to send the message to
    # Replace 'FROM_NUMBER' with your Twilio phone number
    client.messages.create(
        body=message,
        from_='FROM_NUMBER',
        to='TO_NUMBER'
    )

if __name__ == '__main__':
    app.run()

