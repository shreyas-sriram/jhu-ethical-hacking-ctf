from functools import wraps

from flask import Flask, render_template, render_template_string, redirect, url_for, request
from jinja2.exceptions import TemplateSyntaxError
import jwt
import requests

app = Flask(__name__)

GUEST_PASSWORD = 'grooooooooT' # password from forensics challenge
ADMIN_PASSWORD = '0zhleez49l0u4zh4212nt1han0ir2525' # long string that cannot be guessed
JWT_SECRET = 'secret'
JWT_SECRET_ENDPOINT = 'http://localhost:3000/.secret'

# authentication decorator for private routes
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'auth' not in request.cookies and request.path == '/account':
            return redirect(url_for('login'))
        
        if 'auth' not in request.cookies:
            return f(None, *args, **kws)

        user = None
        jwt_token = request.cookies['auth']

        try:
            secret_endpoint = jwt.decode(jwt_token, options={"verify_signature": False})['key']
            secret = requests.get(secret_endpoint).text
            user = jwt.decode(jwt_token, secret, algorithms=['HS256'])['user']
        except:
            if request.path == '/login':
                return f(None, *args, **kws)
            return redirect(url_for('login'))

        if user in ['guest', 'admin']:
            return f(user, *args, **kws)
        else:
            return redirect(url_for('login'))

    return decorated_function

@app.route("/", methods=['GET'])
@authorize
def home(user):
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
@authorize
def login(user):
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if username == 'admin':
            error = 'Admin account can be accessed only through other means. Please contact IT department.'
        elif username != 'guest' or password != GUEST_PASSWORD:
            error = 'Invalid Credentials. Please try again.'
        else:
            secret = requests.get(JWT_SECRET_ENDPOINT).text
            jwt_token = jwt.encode({"user": username, "key": JWT_SECRET_ENDPOINT}, secret, algorithm="HS256")
            
            res = redirect(url_for('account'))
            res.set_cookie('auth', jwt_token)
            return res

    if user:
        return redirect(url_for('account'))
    
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():
    res = redirect(url_for('home'))
    res.delete_cookie('auth')
    return res

@app.route("/account", methods=['GET', 'POST'])
@authorize
def account(user):
    api = None
    
    if request.method == 'POST':
        api = request.form['api'] or None

        rendered_template = render_template("account.html", user=user, api=api)

        try:
            render_template_string(rendered_template)
        except TemplateSyntaxError:
            rendered_template = render_template("account.html", user=user, api='invalid endpoint.')
        finally:
            return render_template_string(rendered_template)

    return render_template('account.html', user=user, api=api)

@app.errorhandler(404)
def four_oh_four(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False)
