from flask import Flask, render_template, request, redirect, url_for, flash
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Route to show the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle login, group message, and file upload
@app.route('/login', methods=['POST'])
def login_and_send_message():
    username = request.form['username']
    password = request.form['password']
    group_chat_id = request.form['group_chat_id']
    delay = int(request.form['delay'])

    # File handling (e.g., txt files with messages to send)
    file = request.files['message_file']
    if not file or file.filename == '':
        flash("No file selected", "error")
        return redirect(url_for('index'))
    
    file_content = file.read().decode('utf-8')

    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open Instagram login page
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)

        # Locate the username and password fields and log in
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)

        # Wait for the login to complete (adjust time based on network speed)
        time.sleep(5)

        # Navigate to direct messages (Group chat ID is needed here)
        driver.get(f'https://www.instagram.com/direct/inbox/')
        time.sleep(2)

        # Locate the group chat and click it (the selector might need adjustment)
        group_chat = driver.find_element(By.XPATH, f"//div[contains(@class, 'MTXfT') and @aria-label='{group_chat_id}']")
        group_chat.click()

        # Wait for the chat to open
        time.sleep(2)

        # Locate the message input box and send the message
        message_box = driver.find_element(By.XPATH, "//textarea[@placeholder='Message...']")
        message_box.send_keys(file_content)  # Send the content from the file
        message_box.send_keys(Keys.RETURN)

        # Wait for the message to be sent
        time.sleep(delay)

        # Close the driver after sending the message
        driver.quit()

        flash("Message sent successfully!", "success")
        return redirect(url_for('index'))

    except Exception as e:
        driver.quit()
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
        
