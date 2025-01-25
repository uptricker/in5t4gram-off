from flask import Flask, request, render_template, redirect, url_for, flash
from instagram_private_api import Client, ClientError
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Instagram Group Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                label {
                    font-weight: bold;
                    margin-top: 10px;
                    display: block;
                }
                input, button {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                .flash-message {
                    color: red;
                    font-weight: bold;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Instagram Group Message Sender</h1>
                {% with messages = get_flashed_messages() %}
                  {% if messages %}
                    <div class="flash-message">{{ messages[0] }}</div>
                  {% endif %}
                {% endwith %}
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="username">Instagram Username:</label>
                    <input type="text" id="username" name="username" required>
                    
                    <label for="password">Instagram Password:</label>
                    <input type="password" id="password" name="password" required>
                    
                    <label for="group_id">Target Group Chat ID:</label>
                    <input type="text" id="group_id" name="group_id" required>
                    
                    <label for="message_file">Select Message File (TXT):</label>
                    <input type="file" id="message_file" name="message_file" accept=".txt" required>
                    
                    <label for="delay">Delay Between Messages (in seconds):</label>
                    <input type="number" id="delay" name="delay" min="1" value="5" required>
                    
                    <button type="submit">Send Messages</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    try:
        username = request.form['username']
        password = request.form['password']
        group_id = request.form['group_id']
        delay = int(request.form['delay'])

        # Save the uploaded file
        message_file = request.files['message_file']
        if not message_file or not message_file.filename.endswith('.txt'):
            flash('Please upload a valid .txt file containing messages.')
            return redirect(url_for('index'))
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], message_file.filename)
        message_file.save(file_path)

        # Read messages from the file
        with open(file_path, 'r') as file:
            messages = [line.strip() for line in file if line.strip()]

        if not messages:
            flash('The message file is empty.')
            return redirect(url_for('index'))

        # Log in to Instagram
        api = Client(username, password)

        # Send messages
        for index, message in enumerate(messages):
            try:
                api.direct_message(group_id, message)
                print(f"[{index + 1}] Message sent: {message}")
                time.sleep(delay)
            except ClientError as e:
                print(f"Failed to send message: {message}. Error: {e}")
                continue

        flash('All messages sent successfully!')
    except Exception as e:
        print(f"An error occurred: {e}")
        flash(f"An error occurred: {e}")
    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
