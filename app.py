from flask import Flask, request, render_template, redirect, url_for, jsonify
from instabot import Bot
import os
import time

app = Flask(__name__)

# Directory to store temporary files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Group Chat Message Sender</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 400px;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            .form-control {
                margin-bottom: 15px;
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .btn {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 15px;
                cursor: pointer;
                border-radius: 5px;
                width: 100%;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Instagram Message Sender</h2>
            <form action="/send" method="post" enctype="multipart/form-data">
                <input type="text" name="username" class="form-control" placeholder="Instagram Username" required>
                <input type="password" name="password" class="form-control" placeholder="Instagram Password" required>
                <input type="text" name="group_id" class="form-control" placeholder="Target Group Chat ID" required>
                <textarea name="message" class="form-control" placeholder="Message to Send"></textarea>
                <label>Select a .txt File (optional):</label>
                <input type="file" name="message_file" class="form-control" accept=".txt">
                <input type="number" name="delay" class="form-control" placeholder="Delay in Seconds" required>
                <button type="submit" class="btn">Send Messages</button>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route('/send', methods=['POST'])
def send_message():
    try:
        # Get form inputs
        username = request.form['username']
        password = request.form['password']
        group_id = request.form['group_id']
        message = request.form['message']
        delay = int(request.form['delay'])

        # Check if a file was uploaded
        if 'message_file' in request.files and request.files['message_file'].filename:
            file = request.files['message_file']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Read messages from the uploaded file
            with open(file_path, 'r') as f:
                messages = f.read().splitlines()
        else:
            # Use the single message provided
            messages = [message]

        # Log in to Instagram using instabot
        bot = Bot()
        bot.login(username=username, password=password)

        # Send messages to the target group chat
        for msg in messages:
            bot.send_message(msg, [group_id])
            print(f"Sent: {msg}")
            time.sleep(delay)

        return jsonify({"status": "success", "message": "Messages sent successfully!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
