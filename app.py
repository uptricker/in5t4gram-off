from flask import Flask, request, render_template, jsonify
from instagrapi import Client
import time
import os

app = Flask(__name__)
cl = Client()
logged_in = False

# Home page
@app.route("/", methods=["GET", "POST"])
def home():
    global logged_in
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            cl.login(username, password)
            logged_in = True
            return "Logged in successfully! <a href='/send_message'>Go to message page</a>"
        except Exception as e:
            return f"Login failed: {e}"
    return '''
        <form method="post">
            <h1>Instagram Login</h1>
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Message sending page
@app.route("/send_message", methods=["GET", "POST"])
# Message sending page
@app.route("/send_message", methods=["GET", "POST"])
def send_message():
    if not logged_in:
        return "You need to login first! <a href='/'>Go to login page</a>"
    
    if request.method == "POST":
        group_id = request.form["group_id"]
        message = request.form["message"]
        delay = int(request.form["delay"])
        file = request.files.get("file")
        
        messages = []
        if file:
            file_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(file_path)
            with open(file_path, "r") as f:
                messages = f.readlines()
        
        try:
            # Send messages from file (if provided) or single message
            if messages:
                for msg in messages:
                    cl.direct_send(msg.strip(), [group_id])  # Using correct API call
                    time.sleep(delay)  # Delay between messages
            else:
                cl.direct_send(message, [group_id])  # Using correct API call
            
            return "Message(s) sent successfully!"
        except Exception as e:
            return f"Failed to send message: {e}"
    return '''
        <form method="post" enctype="multipart/form-data">
            <h1>Send Message</h1>
            Group Chat ID: <input type="text" name="group_id"><br>
            Message: <input type="text" name="message"><br>
            Delay (seconds): <input type="number" name="delay" value="1"><br>
            TXT File (optional): <input type="file" name="file"><br>
            <input type="submit" value="Send">
        </form>
    '''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
