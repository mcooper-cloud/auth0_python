"""Python Flask WebApp Auth0 integration example
"""
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__, static_url_path='/public', static_folder='./public')

import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


AUTH0_CALLBACK_URL = env.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
AUTH0_BASE_URL = 'https://{}'.format(AUTH0_DOMAIN)
AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')
SECRET_KEY = env.get('SECRET_KEY')
PROFILE_KEY = env.get('PROFILE_KEY')
JWT_PAYLOAD = env.get('JWT_PAYLOAD')

#app = Flask(__name__, static_url_path='/public', static_folder='./public')
#app.secret_key = constants.SECRET_KEY
app.secret_key = SECRET_KEY
app.debug = True

auth0_data = None


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url='{}/oauth/token'.format(AUTH0_BASE_URL),
    authorize_url='{}/authorize'.format(AUTH0_BASE_URL),
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():

    token = auth0.authorize_access_token()

    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[JWT_PAYLOAD] = userinfo
    session[PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect('{}/v2/logout?{}'.format(auth0.api_base_url, urlencode(params)))


@app.route('/dashboard')
@requires_auth
def dashboard():

    auth0_data = auth0.__dict__

    if 'email_verified' in session[JWT_PAYLOAD]:
        email_verified = session[JWT_PAYLOAD]['email_verified']
    else:
        email_verified = False

    try:
        return render_template( 'dashboard.html',
                                email_verified=email_verfiied,
                                userinfo=session[PROFILE_KEY],
                                userinfo_pretty=json.dumps(session[JWT_PAYLOAD], indent=4))

    except Exception as e:

        ##
        ## this can happen when reciving profile data from SAML connecitons
        ##
        return render_template('error.html', message=e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
