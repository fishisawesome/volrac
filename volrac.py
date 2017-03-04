from flask import Flask, render_template, request

import os

app = Flask(__name__)

@app.route('/')
def index():
	message = 'Hello world!'
	return render_template('index.html', message=message)

if __name__ == "__main__":
	app.run(host='0.0.0.0')