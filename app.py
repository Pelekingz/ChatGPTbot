import os
import requests
from flask import Flask, request,render_template
import openai
from vonage import Client, Sms




app = Flask(__name__)

client = Client(key='608b3b04', secret='N9FCQ1M9pZhtDfmM')


@app.route('/')
def home():
    return render_template('index.html')
    
# Endpoint to handle incoming messages from WhatsApp
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract the message content from the incoming request
    message = data['messages'][0]['body']
    sender = data['messages'][0]['sender']

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

def send_message(sender, message):

     # Use Vonage API to send the message back to the sender
    sms = Sms(client)
    sms.send_message({
        'from': '0740458874',  # Your Vonage phone number
        'to': sender,  # Phone number of the sender
        'text': message  # Response message
    })


if __name__ == '__main__':
    app.run()

