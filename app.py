from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
import json
import os
import base64
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

@app.route('/dial', methods=['GET', 'POST'])
def create_call():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')

        # Debug: Print the phone number received
        print(f"Received phone number: {phone_number}")

        if not phone_number.startswith('+') or not phone_number[1:].isdigit():
            return "Invalid phone number format. Please use E.164 format.", 400

        space_name = os.getenv('SPACE_NAME')
        project_id = os.getenv('PROJECT_ID')
        auth_token = os.getenv('AUTH_TOKEN')
        from_number = os.getenv('FROM_NUMBER')

        # Debug: Print environment variables
        print(f"Space Name: {space_name}, Project ID: {project_id}")

        url = f'https://{space_name}.signalwire.com/api/calling/calls'
        swml_url = os.getenv('SWML_URL')

        payload = {
            'command': 'dial',
            'params': {
                'from': from_number,
                'to': phone_number,
                'caller_id': from_number,
                'url': swml_url
            }
        }

        # Debug: Print full request details
        print("\n=== REQUEST DETAILS ===")
        print(f"URL: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print(f"Project ID: {project_id}")
        print(f"Auth Token (last 4): ****{auth_token[-4:]}")
        
        # Create the auth header manually
        auth_string = f"{project_id}:{auth_token}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_auth}'
        }
        print(f"Headers: {json.dumps(headers, indent=2)}")

        try:
            response = requests.post(
                url, 
                headers=headers,
                json=payload
            )

            # Debug: Print full response details
            print("\n=== RESPONSE DETAILS ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print("Response Content:")
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text)

            # Check if the response contains valid JSON
            try:
                response_data = response.json()
                return jsonify(response_data)
            except requests.exceptions.JSONDecodeError:
                return f"Server response (Status {response.status_code}): {response.text}", response.status_code

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return f"Request failed: {str(e)}", 500

    return render_template('dial_form.html')

if __name__ == '__main__':
    app.run(debug=True)
