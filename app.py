from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time
import threading

# Flask app setup
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global flag for stopping the process
stop_flag = False

# HTML Template with colorful background and Stop button
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2c3e50;
            color: #ecf0f1;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #34495e;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #1abc9c;
        }
        label {
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        input, select {
            background-color: #ecf0f1;
            color: #2c3e50;
        }
        button {
            background-color: #1abc9c;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #16a085;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: #1abc9c;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="choice">Send To:</label>
            <select id="choice" name="choice" required>
                <option value="group">Group Chats</option>
                <option value="inbox">Inbox</option>
            </select>

            <label for="target_ids">Target IDs (comma-separated):</label>
            <input type="text" id="target_ids" name="target_ids" placeholder="Enter group IDs or usernames" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
        <form action="/stop" method="POST">
            <button class="stop-button" type="submit">Stop Sending</button>
        </form>
    </div>
</body>
</html>
'''

# Function to send messages
def send_messages(username, password, target_ids, messages, choice, delay):
    global stop_flag
    stop_flag = False
    try:
        cl = Client()
        print("[INFO] Logging into Instagram...")
        cl.login(username, password)
        print("[SUCCESS] Logged in!")

        targets = target_ids.split(",")

        for target in targets:
            if stop_flag:
                print("[INFO] Sending stopped by user.")
                break

            for message in messages:
                if stop_flag:
                    print("[INFO] Sending stopped by user.")
                    break

                if choice == "group":
                    print(f"[INFO] Sending to group {target.strip()}: {message}")
                    cl.direct_send(message, thread_ids=[target.strip()])
                elif choice == "inbox":
                    print(f"[INFO] Sending to user {target.strip()}: {message}")
                    cl.direct_send(message, usernames=[target.strip()])

                print("[SUCCESS] Message sent.")
                time.sleep(delay)

        if not stop_flag:
            print("[INFO] All messages sent successfully!")

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

# Flask route for sending messages
@app.route("/", methods=["GET", "POST"])
def instagram_messenger():
    if request.method == "POST":
        global stop_flag
        stop_flag = False
        try:
            # Form data
            username = request.form["username"]
            password = request.form["password"]
            choice = request.form["choice"]
            target_ids = request.form["target_ids"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("instagram_messenger"))

            # Start sending in a background thread
            threading.Thread(target=send_messages, args=(username, password, target_ids, messages, choice, delay)).start()
            flash("Messages are being sent in the background!", "success")

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
    
    return render_template_string(HTML_TEMPLATE)

# Flask route to stop sending
@app.route("/stop", methods=["POST"])
def stop_sending():
    global stop_flag
    stop_flag = True
    flash("Message sending stopped.", "info")
    return redirect(url_for("instagram_messenger"))

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
