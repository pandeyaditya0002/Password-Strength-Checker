from flask import Flask, render_template, request, jsonify
import string
import math

app = Flask(__name__)

def calculate_entropy(password):
    """Calculates entropy based on character diversity and length."""
    charset_size = 0
    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)
    if any(c.isspace() for c in password):
        charset_size += 1
    
    return len(password) * math.log2(charset_size) if charset_size else 0

def check_password_strength(password):
    """Evaluates password strength based on entropy and diversity."""
    entropy = calculate_entropy(password)

    if entropy < 28:
        return {"strength": "Very Weak", "color": "red"}
    elif entropy < 36:
        return {"strength": "Weak", "color": "orange"}
    elif entropy < 60:
        return {"strength": "Moderate", "color": "yellowgreen"}
    elif entropy < 80:
        return {"strength": "Strong", "color": "green"}
    else:
        return {"strength": "Very Strong", "color": "darkgreen"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    password = data.get("password", "")
    result = check_password_strength(password)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
