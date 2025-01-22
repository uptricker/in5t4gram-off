from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

app = Flask(__name__)

# Path to your ChromeDriver
CHROMEDRIVER_PATH = "chromedriver"

@app.route('/')
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Instagram Group Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f7f7f7;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 50px auto;
                    background: #fff;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                }
                h2 {
                    text-align: center;
                    color: #333;
                }
                form {
                    display: flex;
                    flex-direction: column;
                }
                label {
                    margin-bottom: 5px;
                    color: #555;
                }
                input, button {
                    margin-bottom: 15px;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    background: #007BFF;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Instagram Group Message Sender</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="username">Instagram Username:</label>
                    <input type="text" id="username" name="username" required>
                    
                    <label for="password">Instagram Password:</label>
                    <input type="password" id="password" name="password" required>
                    
                    <label for="group_id">Group Chat ID:</label>
                    <input type="text" id="group_id" name="group_id" required>
                    
                    <label for="message_file">Upload Message File (Notepad - .txt):</label>
                    <input type="file" id="message_file" name="message_file" accept=".txt" required>
                    
                    <label for="delay">Delay Between Messages (in seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" min="1" required>
                    
                    <button type="submit">Start Messaging</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    # Get form data
    username = request.form['username']
    password = request.form['password']
    group_id = request.form['group_id']
    delay = int(request.form['delay'])

    # Process uploaded file
    message_file = request.files['message_file']
    messages = message_file.read().decode().splitlines()

    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)

    try:
        # Navigate to Instagram Login
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        # Log in
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(5)

        # Navigate to group chat
        group_chat_url = f"https://www.instagram.com/direct/t/{group_id}/"
        driver.get(group_chat_url)
        time.sleep(5)

        # Send messages
        for message in messages:
            message_box = driver.find_element(By.TAG_NAME, "textarea")
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            print(f"Message sent: {message}")
            time.sleep(delay)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

    return "Messages sent successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
