import requests
import urllib
from flask import Flask, request, redirect
import json
import os

# Flask App definition
app = Flask(__name__)

# Constants
CALLBACK_URL = "/access"
HOSTNAME = "YOUR-HOSTNAME"
CLIENT_ID = "YOUR-CLIENT-ID"
CLIENT_SECRET = "YOUR-CLIENT-SECRET"
JB_OAUTH_URL = "https://jawbone.com/auth/oauth2/auth"
JB_OAUTH_TOKEN_URL = "https://jawbone.com/auth/oauth2/token"
AUTH_URL = None

def generate_auth_url():
    """
        Generates the OAuth url that the client needs to access.
    """
    redirect_uri = 'http://' + HOSTNAME + CALLBACK_URL
    params = {}
    params['response_type']='code'
    params['client_id'] = CLIENT_ID
    params['scope'] = 'basic_read'
    params['redirect_uri'] = redirect_uri
    return JB_OAUTH_URL + "?" + urllib.urlencode(params)

@app.route('/')
def index():
    """
        Index endpoint.
    """
    if not AUTH_URL: # Lazy initialization
        auth_url = generate_auth_url()
    return redirect(auth_url)

@app.route(CALLBACK_URL)
def callback():
    """
       Callback endpoint.
    """
    code = request.args.get('code', '')
    response = request_token(code)
    response_parsed = json.loads(response)
    return "Your Token: " + response_parsed.get("access_token")

def request_token(code):
    """
        Requests authorization token to the Jawbone server
        using the given code and app information.
    """
    params = {}
    params['client_id'] = CLIENT_ID
    params['client_secret'] = CLIENT_SECRET
    params['grant_type'] = "authorization_code"
    params['code'] = code

    # In a production environment, this should be done
    # using a POST request to hide secret information
    url = JB_OAUTH_TOKEN_URL + "?" + urllib.urlencode(params)
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) # Since we are running on heroku, we need to use the port from the environment variable PORT
    app.run(host="0.0.0.0", port=port, debug=True)
