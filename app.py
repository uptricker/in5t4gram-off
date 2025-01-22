from flask import Flask, request, render_template_string, redirect, url_for, flash
import os
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# HTML for the webpage
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JACK INSTA SERVER</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: blue;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: pink;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: pink;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: pink;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            background-color: yellow;
        }
        input:focus, select:focus, button:focus {
            outline: none;
            border-color: pink;
            box-shadow: 0 0 5px rgba(255, 105, 180, 0.5);
        }
        button {
            background-color: pink;
            color: blue;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #ff69b4;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OFLINE INSTAGRAM SERVER</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="choice">Send To:</label>
            <select id="choice" name="choice" required>
                <option value="inbox">Inbox</option>
                <option value="group">Group</option>
            </select>

            <label for="target_username">Target Username (for Inbox):</label>
            <input type="text" id="target_username" name="target_username" placeholder="Enter target username">

            <label for="thread_id">Thread ID (for Group):</label>
            <input type="text" id="thread_id" name="thread_id" placeholder="Enter group thread ID">

            <label for="haters_name">Haters Name:</label>
            <input type="text" id="haters_name" name="haters_name" placeholder="Enter hater's name" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Extract form data
        username = request.form.get("username")
        password = request.form.get("password")
        choice = request.form.get("choice")
        target_username = request.form.get("target_username")
        thread_id = request.form.get("thread_id")
        haters_name = request.form.get("haters_name")
        delay = int(request.form.get("delay"))

        # Handle file upload
        message_file = request.files.get("message_file")
        if message_file and message_file.filename:
            messages = message_file.read().decode().splitlines()
        else:
            flash("Message file is required.", "error")
            return redirect(url_for("home"))

        # Log input data (for debugging purposes)
        print(f"Username: {username}, Target: {target_username or thread_id}, Haters: {haters_name}, Delay: {delay}s")

        # Placeholder for processing logic
        # This is where you'd interact with Instagram's API or your automation logic
        for i, message in enumerate(messages):
            print(f"Sending message {i+1}: {haters_name} {message}")
            time.sleep(delay)  # Simulate delay between messages

        flash("Messages sent successfully!", "success")
        return redirect(url_for("home"))

    return render_template_string(HTML_PAGE)


if __name__ == "__main__":
    # Run the Flask app on localhost at port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
        
