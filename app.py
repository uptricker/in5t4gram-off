from flask import Flask, request, render_template, redirect, url_for, flash
import instaloader
import time
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your own secret key


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
                padding: 20px;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .form-control {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .btn {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 5px;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Instagram Group Message Sender</h2>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="username">Instagram Username:</label>
                <input type="text" name="username" id="username" class="form-control" required>
                
                <label for="password">Instagram Password:</label>
                <input type="password" name="password" id="password" class="form-control" required>
                
                <label for="group_id">Target Group Chat ID:</label>
                <input type="text" name="group_id" id="group_id" class="form-control" required>
                
                <label for="message_file">Select Message File (.txt):</label>
                <input type="file" name="message_file" id="message_file" class="form-control" accept=".txt" required>
                
                <label for="delay">Delay Between Messages (seconds):</label>
                <input type="number" name="delay" id="delay" class="form-control" value="5" required>
                
                <button type="submit" class="btn">Send Messages</button>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route('/', methods=['POST'])
def send_messages():
    # Retrieve form data
    username = request.form['username']
    password = request.form['password']
    group_id = request.form['group_id']
    delay = int(request.form['delay'])
    message_file = request.files['message_file']

    # Validate uploaded file
    if not message_file or not message_file.filename.endswith('.txt'):
        flash("Please upload a valid .txt file!")
        return redirect(url_for('index'))

    # Read messages from the uploaded file
    messages = message_file.read().decode('utf-8').splitlines()

    try:
        # Login to Instagram using Instaloader
        loader = instaloader.Instaloader()
        loader.login(username, password)

        # Send messages to the group chat
        for i, message in enumerate(messages):
            print(f"Sending message {i + 1}/{len(messages)}: {message}")
            loader.context.post_message(message, recipients=[group_id])
            time.sleep(delay)

        flash("Messages sent successfully!")
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
    
