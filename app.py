from flask import Flask, request, render_template, redirect, url_for
from instabot import Bot
import time
import os

app = Flask(__name__)

# Path to temporary storage for the uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global bot instance
bot = None

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Instagram Bot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    padding: 20px;
                    margin: 0;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input, button {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #218838;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Instagram Bot</h2>
                <form action="/send_message" method="post" enctype="multipart/form-data">
                    <label for="username">Instagram Username:</label>
                    <input type="text" id="username" name="username" required>

                    <label for="password">Instagram Password:</label>
                    <input type="password" id="password" name="password" required>

                    <label for="group_id">Target Group Chat ID:</label>
                    <input type="text" id="group_id" name="group_id" required>

                    <label for="message_file">Select Message File (TXT):</label>
                    <input type="file" id="message_file" name="message_file" accept=".txt" required>

                    <label for="delay">Delay Between Messages (seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" required>

                    <button type="submit">Send Messages</button>
                </form>
            </div>
        </body>
    </html>
    '''

@app.route('/send_message', methods=['POST'])
def send_message():
    global bot
    username = request.form.get('username')
    password = request.form.get('password')
    group_id = request.form.get('group_id')
    delay = int(request.form.get('delay'))

    # Save the uploaded file
    message_file = request.files['message_file']
    file_path = os.path.join(UPLOAD_FOLDER, message_file.filename)
    message_file.save(file_path)

    # Read messages from the file
    with open(file_path, 'r') as file:
        messages = file.readlines()

    try:
        # Log in to Instagram
        bot = Bot()
        bot.login(username=username, password=password)

        # Send messages to the group
        for index, message in enumerate(messages):
            message = message.strip()
            if not message:
                continue
            bot.send_message(message, [group_id])
            print(f"[{index + 1}] Message sent: {message}")
            time.sleep(delay)

        return "Messages sent successfully!"
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Clean up files and logout
        if bot:
            bot.logout()
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
