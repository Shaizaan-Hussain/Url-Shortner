# 🔗 URL Shortener

A simple and minimal Flask-based URL shortening service, inspired by Bitly and TinyURL. It allows users to shorten long URLs, redirect using short codes, and track analytics like click count and creation timestamp.

---

## 🚀 Features

- ✅ Shorten long URLs to unique 6-character codes
- 🔁 Redirect users to original URLs via short code
- 📊 View analytics: click count, created time, original URL
- 🧠 Thread-safe in-memory storage
- ✅ Fully tested with `pytest`

---

## 📦 Tech Stack

- Python 3.8+
- Flask
- Pytest

---

## 📁 Project Structure

url-shortener/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── model.py
│ └── util.py
├── tests/
│ └── test.py
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## ⚙️ Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
2. Setup virtual environment
bash
Copy
Edit
python -m venv venv
# Activate on Windows
venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Start the Flask server
bash
Copy
Edit
python -m flask --app app.main run
The API will run at: http://localhost:5000

🔌 API Endpoints
1. Shorten URL
POST /api/shorten

json
Copy
Edit
Request:
{
  "url": "https://www.example.com"
}

Response:
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}
2. Redirect to Original URL
GET /abc123

Redirects to https://www.example.com.

3. Get Analytics
GET /api/stats/abc123

json
Copy
Edit
{
  "url": "https://www.example.com",
  "clicks": 5,
  "created_at": "2025-07-24T10:00:00"
}
🧪 Run Tests
bash
Copy
Edit
pytest
🙌 Contribution
Feel free to fork, clone, and open pull requests! Suggestions and improvements are always welcome.

📄 License
This project is open source and available under the MIT License.

yaml
Copy
Edit

---

Let me know if you want me to also generate a `requirements.txt` or `LICENSE` file.








Ask ChatGPT
You said:
make it one file


ChatGPT said:
Here is the entire URL shortener project in a single file (main.py), combining all logic (shortening, redirection, analytics, utils, and storage) for ease of setup and execution.

✅ main.py
python
Copy
Edit
from flask import Flask, request, jsonify, redirect
from datetime import datetime
import string
import random
import re

app = Flask(__name__)
store = {}

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    regex = re.compile(
        r'^(https?://)?'  # optional scheme
        r'(([A-Za-z_0-9.-]+)\.([A-Za-z]{2,}))'  # domain
        r'(\:[0-9]+)?'  # optional port
        r'(\/.*)?$', re.IGNORECASE)  # path
    return re.match(regex, url)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url or not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_short_code()
    while short_code in store:
        short_code = generate_short_code()

    store[short_code] = {
        'url': original_url if original_url.startswith('http') else 'https://' + original_url,
        'created_at': datetime.utcnow(),
        'clicks': 0
    }

    return jsonify({
        'short_code': short_code,
        'short_url': request.host_url + short_code
    })

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    if short_code not in store:
        return jsonify({'error': 'Short URL not found'}), 404

    store[short_code]['clicks'] += 1
    return redirect(store[short_code]['url'], code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    if short_code not in store:
        return jsonify({'error': 'Short code not found'}), 404

    data = store[short_code]
    return jsonify({
        'url': data['url'],
        'clicks': data['clicks'],
        'created_at': data['created_at'].isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the URL Shortener API'}), 200

if __name__ == '__main__':
    app.run(debug=True)
✅ Run Instructions
Save this as main.py

Install Flask:

bash
Copy
Edit
pip install flask
Run the app:

bash
Copy
Edit
python main.py
API is available at: http://127.0.0.1:5000

Let me know if you want the same thing containerized (Docker) or tested with Postman.








You said:
give readme file in one so i can directly paste it


ChatGPT said:
Here's a complete README.md content you can copy-paste directly into your project:

markdown
Copy
Edit
# 🧩 URL Shortener Service

A simple and minimal URL shortening service built with Flask. Similar to services like bit.ly and TinyURL.

## 📦 Features

- ✅ Shorten long URLs to 6-character alphanumeric codes
- 🚀 Redirection from short code to original URL
- 📊 Analytics: click count, creation time, and original URL
- 🔐 URL validation
- 🧪 Simple in-memory storage (no database needed)
- ⚡ Minimal setup (single Python file)

---

## 🏁 Getting Started

### 📌 Prerequisites

- Python 3.8+
- Flask (`pip install flask`)

---

### 🚀 Run the Project

```bash
# Clone or download the project
cd url-shortener

# Install Flask
pip install flask

# Run the app
python main.py
By default, the API runs on:
📍 http://127.0.0.1:5000

📡 API Endpoints
1. Shorten URL
POST /api/shorten

Body:

json
Copy
Edit
{
  "url": "https://www.example.com/very/long/url"
}
Response:

json
Copy
Edit
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}
2. Redirect to Original URL
GET /<short_code>

Example:
GET http://localhost:5000/abc123

Action:
Redirects to original long URL

3. URL Stats
GET /api/stats/<short_code>

Response:

json
Copy
Edit
{
  "url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2025-07-24T10:00:00"
}
🧪 Testing with Postman
POST /api/shorten – Send JSON body with "url" to shorten

GET /<short_code> – Paste short_url in browser or Postman (will redirect)

GET /api/stats/<short_code> – Get analytics of that short link

📂 Project Structure
bash
Copy
Edit
url-shortener/
├── main.py         # All logic in one file
├── README.md       # Project instructions
🙏 Acknowledgements
Built for learning Flask and REST APIs. Ideal for assignments, small-scale use, or as a backend component for frontend integration.

📜 License
MIT License – free to use, share, and modify.

yaml
Copy
Edit

---

Let me know if you want badges (like GitHub stars, forks, etc.) or deployment instructions (like for Heroku, Vercel, or Docker).







