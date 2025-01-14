from flask import Flask, render_template, request, jsonify
from werkzeug.utils import quote  # Use the correct import

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode_url():
    data = request.json
    url = data.get('url', '')
    if url:
        encoded_url = quote(url)  # Encoding the URL with 'quote'
        return jsonify({'encoded_url': encoded_url})
    return jsonify({'error': 'No URL provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
