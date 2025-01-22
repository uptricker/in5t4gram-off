from flask import Flask, request, render_template, redirect, url_for
import time
import os

app = Flask(__name__)

# --- Render Form ---
@app.route('/')
def index():
    return '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Automation</title>
        <style>
            body {
                background-color: #f0f8ff;
                font-family: Arial, sans-serif;
                color: #333;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Instagram Group Message Bot</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="username">Instagram Username:</label>
                <input type="text" id="username" name="username" required>
                
                <label for="password">Instagram Password:</label>
                <input type="password" id="password" name="password" required>
                
                <label for="target_group_id">Target Group Chat ID:</label>
                <input type="text" id="target_group_id" name="target_group_id" required>
                
                <label for="haters_name">Hater's Name:</label>
                <input type="text" id="haters_name" name="haters_name" required>
                
                <label for="messages_file">Select Message File (.txt):</label>
                <input type="file" id="messages_file" name="messages_file" accept=".txt" required>
                
                <label for="delay">Delay (Seconds):</label>
                <input type="number" id="delay" name="delay" value="5" required>
                
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

# --- Process Form Submission ---
@app.route('/', methods=['POST'])
def submit_form():
    username = request.form.get('username')
    password = request.form.get('password')
    target_group_id = request.form.get('target_group_id')
    haters_name = request.form.get('haters_name')
    delay = int(request.form.get('delay'))
    
    # Save uploaded file
    messages_file = request.files['messages_file']
    messages = messages_file.read().decode().splitlines()
    
    # Authenticate Instagram (replace with a valid API or library)
    try:
        # Example: Login (placeholder code)
        print(f"Logging in as {username}...")
        # Simulate successful login
        if username == "test_user" and password == "test_pass":
            print("Login successful!")
        else:
            raise Exception("Invalid credentials.")
        
        # Send messages
        for index, message in enumerate(messages):
            print(f"Sending to group {target_group_id}: {haters_name} {message}")
            time.sleep(delay)  # Delay between messages
            
        print("All messages sent successfully.")
        return "Messages sent successfully! Check your console for details."
    
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}"

# --- Run App ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
