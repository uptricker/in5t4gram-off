from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

app = Flask(__name__)

# Set up the Selenium WebDriver
def init_driver():
    options = Options()
    options.headless = False  # Set to True if you want to run without opening browser
    driver = webdriver.Chrome(service=Service("/path/to/chromedriver"), options=options)
    return driver

# Instagram login function
def instagram_login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)  # Adjust the sleep time if necessary

    # Find the username and password fields and submit them
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
    time.sleep(5)

# Send a message to a group chat
def send_message(driver, group_id, message):
    driver.get(f"https://www.instagram.com/direct/inbox/")
    time.sleep(3)
    
    # Open the conversation by group ID (can be an element such as a class or username)
    group_chat = driver.find_element(By.XPATH, f"//div[contains(@aria-label, '{group_id}')]")
    group_chat.click()
    time.sleep(2)

    # Type and send the message
    message_box = driver.find_element(By.XPATH, "//textarea[@placeholder='Message...']")
    message_box.send_keys(message + Keys.RETURN)
    time.sleep(2)

# Flask route to trigger the Instagram automation
@app.route('/automate', methods=['POST'])
def automate():
    # Get the form data
    username = request.form['username']
    password = request.form['password']
    group_id = request.form['group_id']
    message = request.form['message']
    
    # Initialize the Selenium driver
    driver = init_driver()

    try:
        # Perform Instagram login and send message
        instagram_login(driver, username, password)
        send_message(driver, group_id, message)

        # Close the browser
        driver.quit()
        return jsonify({"status": "success", "message": "Message sent successfully!"})
    except Exception as e:
        driver.quit()
        return jsonify({"status": "error", "message": str(e)})

# Route for file upload (to select txt files)
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file and file.filename.endswith('.txt'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return jsonify({"status": "success", "message": f"File {file.filename} uploaded successfully!"})

    return jsonify({"status": "error", "message": "Only .txt files are allowed!"})

# Run the Flask app on a specified port
if __name__ == '__main__':
    app.run(debug=True, port=5000)
        
