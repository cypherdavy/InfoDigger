from flask import Flask, render_template, request, jsonify
from werkzeug.utils import quote  # Importing the correct function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode_url():
    data = request.json
    url = data.get('url', '')  # Retrieve URL from the request JSON
    if url:
        encoded_url = quote(url)  # URL encoding using quote
        return jsonify({'encoded_url': encoded_url})
    return jsonify({'error': 'No URL provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
