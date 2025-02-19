from flask import Flask, jsonify, request, render_template
import requests
import os
import base64
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv(override=True)

# Global variable to store active call ID
active_call_id = None

@app.route('/')
def index():
    # Pass the active call state to the template
    return render_template('index.html', active_call_id=active_call_id)

@app.route('/dial', methods=['POST'])
def create_call():
    global active_call_id
    
    # If there's already an active call, return error
    if active_call_id:
        return jsonify({'error': 'There is already an active call'}), 400
        
    phone_number = request.form.get('phone_number')
    swml_url = request.form.get('swml_url')
    if not swml_url:
        swml_url = os.getenv('SWML_URL')
    
    space_name = os.getenv('SPACE_NAME')
    project_id = os.getenv('PROJECT_ID')
    auth_token = os.getenv('AUTH_TOKEN')
    from_number = os.getenv('FROM_NUMBER')

    url = f'https://{space_name}.signalwire.com/api/calling/calls'

    payload = {
        'command': 'dial',
        'params': {
            'from': from_number,
            'to': phone_number,
            'caller_id': from_number,
            'url': swml_url
        }
    }

    auth_string = f"{project_id}:{auth_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_auth}'
    }

    try:
        response = requests.post(
            url, 
            headers=headers,
            json=payload
        )

        try:
            response_data = response.json()
            # Store the call ID if the call was successful
            if response.status_code == 200 and 'id' in response_data:
                active_call_id = response_data['id']
            return jsonify(response_data)
        except requests.exceptions.JSONDecodeError:
            return jsonify({'error': f'Server response (Status {response.status_code}): {response.text}'}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

@app.route('/hangup', methods=['POST'])
def hangup_call():
    global active_call_id
    
    # Check if there's an active call
    if not active_call_id:
        return jsonify({'error': 'No active call to hang up'}), 400

    space_name = os.getenv('SPACE_NAME')
    project_id = os.getenv('PROJECT_ID')
    auth_token = os.getenv('AUTH_TOKEN')

    url = f'https://{space_name}.signalwire.com/api/calling/calls'
    
    payload = {
        "id": active_call_id,
        "command": "calling.end",
        "params": {
            "reason": "hangup",
        }
    }
    
    auth_string = f"{project_id}:{auth_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_auth}'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            # Clear the active call ID after successful hangup
            active_call_id = None
        return jsonify(response.json() if response.content else {'status': 'success'})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/message', methods=['POST'])
def message():
    global active_call_id
    
    content = request.form.get('content')
    role = request.form.get('role')
    
    # If there's no active call, return error
    if not active_call_id:
        return jsonify({'error': 'No active call to send message to'}), 400

    space_name = os.getenv('SPACE_NAME')
    project_id = os.getenv('PROJECT_ID')
    auth_token = os.getenv('AUTH_TOKEN')

    url = f'https://{space_name}.signalwire.com/api/calling/calls'
    
    payload = {
        "id": active_call_id,
        "command": "calling.ai_message",
        "params": {
            "role": role,
            "message_text": content
        }
    }
    
    auth_string = f"{project_id}:{auth_token}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_auth}'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return jsonify(response.json() if response.content else {'status': 'success'})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
