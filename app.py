from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def escape_markdown(text):
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!])", r"\\\1", text)

def get_ifsc_details(ifsc_code):
    url = f"https://ifsc.razorpay.com/{ifsc_code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch IFSC details."}


def trace_number(phone_number):
    url = "https://calltracer.in"
    headers = {
        "Host": "calltracer.in",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"country": "IN", "q": phone_number}
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            details = {}
            try:
                details["Number"] = phone_number
                details["Complaints"] = soup.find(text="Complaints").find_next("td").text
                # Add other fields as necessary
            except Exception:
                return {"error": "Unable to extract all details."}
            return details
        else:
            return {"error": f"HTTP Status Code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def whois_lookup(domain):
    url = f"https://ipwhois.app/json/{domain}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve Whois data."}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ifsc', methods=['POST'])
def ifsc_lookup():
    ifsc_code = request.form.get('ifsc_code')
    if not ifsc_code:
        return jsonify({"error": "Please provide an IFSC code."}), 400
    result = get_ifsc_details(ifsc_code)
    return jsonify(result)

@app.route('/phone', methods=['POST'])
def phone_lookup():
    phone_number = request.form.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Please provide a phone number."}), 400
    result = trace_number(phone_number)
    return jsonify(result)

@app.route('/whois', methods=['POST'])
def domain_lookup():
    domain = request.form.get('domain')
    if not domain:
        return jsonify({"error": "Please provide a domain."}), 400
    result = whois_lookup(domain)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
