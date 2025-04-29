# bulk_predict_attack.py

import sys
import pandas as pd
import joblib

# Load model and vectorizer
model = joblib.load('attack_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Check if a filename was provided
if len(sys.argv) != 2:
    print("Usage: python3 bulk_predict_attack.py filename.txt")
    sys.exit(1)

# Get the filename from command line
input_filename = sys.argv[1]

# Read all logs from the input file
try:
    with open(input_filename, 'r') as f:
        logs = f.readlines()
except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    sys.exit(1)

# Clean logs (remove newline characters)
logs = [log.strip() for log in logs if log.strip() != ""]

# Vectorize the logs
logs_vectorized = vectorizer.transform(logs)

# Predict
predictions = model.predict(logs_vectorized)

# Save results to CSV
results = pd.DataFrame({
    'log_message': logs,
    'predicted_attack_type': predictions
})

output_filename = "bulk_predictions.csv"
results.to_csv(output_filename, index=False)

print(f"✅ Bulk prediction complete! Results saved to '{output_filename}'")

