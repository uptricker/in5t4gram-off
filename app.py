from flask import Flask, request, render_template, redirect, url_for
import time
import os
import openai  # Ensure you install `openai` for ChatGPT interaction
from instagrapi import Client  # Install `instagrapi` for Instagram API

app = Flask(__name__)

# OpenAI API Key
openai.api_key = "your-chatgpt-secret-key"

@app.route('/')
def index():
    return '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram ChatBot</title>
        <style>
            body {
                background-color: #1a1a1a;
                color: #f2f2f2;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 500px;
                margin: 50px auto;
                padding: 20px;
                background-color: #333;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }
            .form-control {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #444;
                color: #f2f2f2;
            }
            .btn {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .btn:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Instagram Group Message Bot</h2>
            <form action="/" method="post" enctype="multipart/form-data">
                <input type="text" class="form-control" name="username" placeholder="Instagram Username" required>
                <input type="password" class="form-control" name="password" placeholder="Instagram Password" required>
                <input type="text" class="form-control" name="group_id" placeholder="Target Group Chat ID" required>
                <input type="file" class="form-control" name="message_file" accept=".txt" required>
                <input type="text" class="form-control" name="haters_name" placeholder="Hater's Name" required>
                <input type="number" class="form-control" name="delay" placeholder="Delay in Seconds" min="1" required>
                <button type="submit" class="btn">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    # Fetch form data
    username = request.form.get('username')
    password = request.form.get('password')
    group_id = request.form.get('group_id')
    haters_name = request.form.get('haters_name')
    delay = int(request.form.get('delay'))

    # Handle uploaded file
    message_file = request.files['message_file']
    messages = message_file.read().decode().splitlines()

    # Authenticate with Instagram
    client = Client()
    try:
        client.login(username, password)
    except Exception as e:
        return f"<h3>Instagram Login Failed: {str(e)}</h3>"

    # Send messages to the group chat
    for i, message in enumerate(messages):
        try:
            final_message = f"{haters_name}: {message}"
            client.direct_send(final_message, [group_id])
            time.sleep(delay)  # Wait for the specified delay
        except Exception as e:
            print(f"Failed to send message {i+1}: {e}")
            continue

    return "<h3>Messages sent successfully!</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
