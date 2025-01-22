from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Instagram Bot</title>
            <style>
                body {
                    background-color: #f0f0f0;
                    font-family: Arial, sans-serif;
                }
                .container {
                    max-width: 500px;
                    margin: 50px auto;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                input, button {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border: 1px solid #ccc;
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
                <h2>Instagram Message Bot</h2>
                <form action="/" method="POST" enctype="multipart/form-data">
                    <label>Instagram Username:</label>
                    <input type="text" name="username" required>
                    <label>Instagram Password:</label>
                    <input type="password" name="password" required>
                    <label>Target Group Name:</label>
                    <input type="text" name="group_name" required>
                    <label>Messages File (.txt):</label>
                    <input type="file" name="message_file" accept=".txt" required>
                    <label>Delay (in seconds):</label>
                    <input type="number" name="delay" value="5" required>
                    <button type="submit">Start Bot</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def automate_instagram():
    username = request.form['username']
    password = request.form['password']
    group_name = request.form['group_name']
    delay = int(request.form['delay'])
    message_file = request.files['message_file']
    
    # Read messages from uploaded file
    messages = message_file.read().decode().splitlines()
    
    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode (optional)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path="chromedriver")  # Path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open Instagram login page
        driver.get("https://www.instagram.com/accounts/login/")
        wait = WebDriverWait(driver, 20)
        
        # Log in
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password, Keys.RETURN)
        time.sleep(5)  # Allow time for login

        # Navigate to direct messages
        driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(5)  # Allow inbox to load

        # Find the target group
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        search_box.send_keys(group_name)
        time.sleep(3)  # Allow search results to load
        search_box.send_keys(Keys.RETURN, Keys.RETURN)  # Open the chat
        time.sleep(5)

        # Send messages from the file
        for message in messages:
            text_area = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            text_area.send_keys(message, Keys.RETURN)
            time.sleep(delay)

        return "Messages sent successfully!"
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
