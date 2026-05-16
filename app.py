import os
import time
import json
from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from playwright.sync_api import sync_playwright

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- HTML & JavaScript for the Terminal UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Isaahi Terminal</title>
    <style>
        body { background-color: black; color: #00ff00; font-family: 'Courier New', Courier, monospace; padding: 20px; }
        input { background: transparent; border: none; color: #00ff00; font-family: 'Courier New', Courier, monospace; font-size: 16px; outline: none; width: 80%; }
        .output { margin-bottom: 10px; white-space: pre-wrap;}
    </style>
</head>
<body>
    <div id="terminal">
        <div class="output">Welcome to the system. Please authenticate.</div>
    </div>
    <span style="color: white;">> </span><input type="text" id="cmd" autofocus autocomplete="off">

    <script>
        let step = 0;
        const terminal = document.getElementById('terminal');
        const input = document.getElementById('cmd');

        function printLine(text, color="#00ff00") {
            terminal.innerHTML += `<div class="output" style="color: ${color};">${text}</div>`;
            window.scrollTo(0, document.body.scrollHeight);
        }

        input.addEventListener('keypress', async function (e) {
            if (e.key === 'Enter') {
                const val = input.value.trim();
                input.value = '';
                printLine(`> ${val}`, "white");

                if (step === 0 && val === "download -itd pro") {
                    printLine("Downloading modules... Done.");
                    step = 1;
                } 
                else if (step === 1 && val === "itd start -isaahi ai agent") {
                    printLine("Initializing Isaahi Core...");
                    step = 2;
                } 
                else if (step === 2 && val === "itd -start") {
                    printLine("ISAAHI AGENT ONLINE.", "cyan");
                    printLine("What would you like Isaahi to do in NautilusOS?");
                    step = 3;
                }
                else if (step === 3) {
                    printLine("Processing request... (Please wait, Isaahi is navigating the OS)", "yellow");
                    
                    // Send the request to the Python backend
                    const response = await fetch('/run-isaahi', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ goal: val })
                    });
                    
                    const data = await response.json();
                    if(data.success) {
                        printLine("Task completed successfully.");
                    } else {
                        printLine("Error: " + data.error, "red");
                    }
                    printLine("What would you like Isaahi to do next?");
                } 
                else {
                    printLine("Command not recognized or out of sequence.", "red");
                }
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/run-isaahi", methods=["POST"])
def execute_isaahi():
    data = request.json
    user_goal = data.get("goal")
    
    # Wrap your original Isaahi Playwright logic here
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://nautilus-os.netlify.app/")
            page.wait_for_timeout(3000)
            
            # --- Insert your Groq/Playwright loop here ---
            # For brevity in this example, we just wait a moment.
            # In your real code, you would call your ask_isaahi() function and click elements.
            time.sleep(2) 
            
            browser.close()
            return jsonify({"success": True})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
