from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.errorhandler(404)
def four_oh_four(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False)
