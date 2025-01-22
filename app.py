from flask import Flask, request, render_template, redirect, url_for
from instagrapi import Client
import os
import time

app = Flask(__name__)

# Path to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return '''
        <html>
        <head>
            <title>Instagram Group Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    padding: 20px;
                    text-align: center;
                }
                .form-container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    margin: auto;
                }
                input, button, label {
                    display: block;
                    width: 100%;
                    margin-bottom: 15px;
                }
                button {
                    background-color: #007bff;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Instagram Group Message Sender</h1>
            <div class="form-container">
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="username">Instagram Username:</label>
                    <input type="text" id="username" name="username" required>
                    
                    <label for="password">Instagram Password:</label>
                    <input type="password" id="password" name="password" required>
                    
                    <label for="apiKey">API Key:</label>
                    <input type="text" id="apiKey" name="apiKey" required>
                    
                    <label for="groupId">Target Group Chat ID:</label>
                    <input type="text" id="groupId" name="groupId" required>
                    
                    <label for="messageFile">Upload Message File (.txt):</label>
                    <input type="file" id="messageFile" name="messageFile" accept=".txt" required>
                    
                    <label for="delay">Delay (in seconds):</label>
                    <input type="number" id="delay" name="delay" min="1" required>
                    
                    <label for="hatersName">Haters Name Prefix:</label>
                    <input type="text" id="hatersName" name="hatersName" required>
                    
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    '''


@app.route('/', methods=['POST'])
def send_messages():
    username = request.form['username']
    password = request.form['password']
    api_key = request.form['apiKey']
    group_id = request.form['groupId']
    delay = int(request.form['delay'])
    haters_name = request.form['hatersName']

    # Save the uploaded message file
    message_file = request.files['messageFile']
    message_file_path = os.path.join(app.config['UPLOAD_FOLDER'], message_file.filename)
    message_file.save(message_file_path)

    # Read messages from the file
    with open(message_file_path, 'r') as file:
        messages = file.readlines()

    # Initialize Instagram Client
    cl = Client()
    try:
        cl.login(username, password)
    except Exception as e:
        return f"Error: Unable to login. {str(e)}"

    # Send messages to the group chat
    for idx, message in enumerate(messages):
        try:
            message_content = f"{haters_name} {message.strip()}"
            cl.direct_send(message_content, [group_id])
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent message {idx + 1}: {message_content}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error sending message {idx + 1}: {str(e)}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
