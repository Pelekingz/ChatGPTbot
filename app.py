import os
import requests
from flask import Flask, request, render_template
import openai
from google.cloud import dialogflow_v2 as dialogflow
import uuid


app = Flask(__name__)


# Configure OpenAI ChatGPT API credentials
openai_api_key = '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'

# Configure Dialogflow credentials
dialogflow_project_id = 'chatgptbot-390815'
dialogflow_session_id = str(uuid.uuid4())
dialogflow_language_code = 'en-US'


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

        # Generate a new session ID for each request
        dialogflow_session_id = str(uuid.uuid4())

        # Call the ChatGPT API to process the message
        response = chat_with_gpt(message)

        # Send the response back to WhatsApp
        send_message(sender, response, dialogflow_session_id)

        return 'Message sent'

    except Exception as e:
        # Handle any exceptions that occur during API calls
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return error_message, 500



def chat_with_gpt(message):
    try:
        # Call the ChatGPT API to generate a response
        gpt_response = requests.post(
            'https://api.openai.com/v1/engines/davinci-codex/completions',
            headers={
                'Authorization': f'Bearer {openai_api_key}',
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

    except requests.exceptions.RequestException as e:
        # Handle API request errors
        raise Exception(f"ChatGPT API request failed: {str(e)}")

    except (KeyError, IndexError) as e:
        # Handle JSON parsing errors
        raise Exception(f"Invalid API response format: {str(e)}")


def send_message(sender, message):
    try:
        # Initialize the Dialogflow session client
        session_client = dialogflow.SessionsClient()

        # Create the Dialogflow session path
        session_path = session_client.session_path(dialogflow_project_id, dialogflow_session_id)

        # Create the text input for the Dialogflow session
        text_input = dialogflow.TextInput(text=message, language_code=dialogflow_language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        # Send the message to Dialogflow and receive the response
        response = session_client.detect_intent(
            request={"session": session_path, "query_input": query_input}
        )

        # Extract the Dialogflow response
        dialogflow_response = response.query_result.fulfillment_text

        # Use Dialogflow's response as the final response
        final_response = dialogflow_response

        # Use Vonage API to send the message back to the sender (WhatsApp)
        # Implement your Vonage code here

        return final_response

    except Exception as e:
        # Handle any exceptions that occur during API calls
        raise Exception(f"Failed to send message: {str(e)}")


if __name__ == '__main__':
    app.run()


