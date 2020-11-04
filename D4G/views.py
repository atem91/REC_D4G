from flask import Flask

app = Flask(__name__)

app.config.from_object('D4G.config')


@app.route('/')
def index():
    return "Hello world!"
