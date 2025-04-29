# predict_attack.py

import sys
import joblib

# Load the saved model and vectorizer
model = joblib.load('attack_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Check if user gave a log message
if len(sys.argv) != 2:
    print("Usage: python3 predict_attack.py 'your log message here'")
    sys.exit(1)

# Get the log message from command line
log_message = [sys.argv[1]]

# Vectorize the log message
log_vectorized = vectorizer.transform(log_message)

# Predict the attack type
predicted_attack_type = model.predict(log_vectorized)

# Output the result
print("Predicted Attack Type:", predicted_attack_type[0])

