# Flask Call Dialer

This is a Flask web application that allows users to initiate phone calls using the SignalWire API. The application provides a simple web interface where users can input a phone number, and the server will attempt to create a call to that number using the SignalWire platform.

## Features

- **Web Interface**: A simple form to input the phone number to dial.
- **SignalWire Integration**: Utilizes the SignalWire REST API to create calls.
- **Environment Configuration**: Uses environment variables to manage sensitive information like API credentials.

## Prerequisites

- Python 3.x
- Flask
- Requests library
- Python-dotenv

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   SPACE_NAME=<your_signalwire_space_name>
   PROJECT_ID=<your_signalwire_project_id>
   AUTH_TOKEN=<your_signalwire_auth_token>
   FROM_NUMBER=<your_signalwire_from_number>
   SWML_URL=<your_signalwire_swml_url>
   ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   Open your web browser and go to `http://localhost:5000/dial`.

3. **Make a call**:
   Enter the phone number in E.164 format (e.g., +1234567890) and submit the form to initiate a call.

## SignalWire API

This application uses the [SignalWire REST API](https://developer.signalwire.com/rest/signalwire-rest/endpoints/calling/calls-create) to create calls. The API requires a POST request to the `/calls` endpoint with a payload that includes a `dial` command and additional parameters such as the `from` and `to` phone numbers.

## Debugging

The application includes debug print statements to help trace the flow of data and identify issues. These can be found in the `create_call` function within `app.py`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SignalWire](https://signalwire.com) for providing the API and documentation.
