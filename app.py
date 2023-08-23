import os
import requests
from flask import Flask, request, render_template
import openai
from messagebird import Client, Message

app = Flask(__name__)

# Configure MessageBird API credentials
messagebird_api_key = 'bglasQBrh5JflgeffZ5nAviqt'
messagebird_phone_number = '0740458874'

messagebird_client = Client(messagebird_api_key)

# Configure OpenAI ChatGPT API credentials
openai_api_key = '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'

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to handle incoming messages from WhatsApp
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    try:
        # Extract the message content from the incoming request
        message = data['messages'][0]['body']
        sender = data['messages'][0]['sender']

        # Call the ChatGPT API to process the message
        response = chat_with_gpt(message)

        # Send the response back using MessageBird
        send_message(sender, response)

        return 'Message sent'

    except Exception as e:
        # Handle any exceptions that occur during the process
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return error_message, 500

def chat_with_gpt(message):
    try:
        # Call the ChatGPT API to generate a response
        gpt_response = openai.Completion.create(
            engine="davinci-codex",
            prompt=message,
            max_tokens=50,
            api_key=openai_api_key
        )

        # Extract the generated response from the API response
        response = gpt_response.choices[0].text

        return response

    except openai.error.OpenAIError as e:
        # Handle API request errors
        raise Exception(f"ChatGPT API request failed: {str(e)}")

def send_message(sender, message):
    try:
        # Use MessageBird API to send the message back to the sender
        response = messagebird_client.message_create(
            messagebird_phone_number,
            [sender],
            message
        )
        
        if response.recipients.totalSentCount == 1:
            print("Message sent successfully.")
        else:
            print("Message delivery to recipient failed.")
            # You can choose to log, retry, or handle the failure in a way that suits your application.

    except messagebird.client.ErrorException as e:
        # Handle MessageBird API errors
        error_message = f"Failed to send message: {str(e)}"
        print(error_message)
        # You might want to log the error and possibly take further action based on the specific error.

    except Exception as e:
        # Handle any other exceptions that occur during the process
        error_message = f"An error occurred while sending the message: {str(e)}"
        print(error_message)
        # You might want to log the error and possibly take further action based on the specific error.


if __name__ == '__main__':
    app.run()




