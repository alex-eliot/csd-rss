import threading
from flask import Flask
import bot

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>sup</p>"

@app.route("/ping")
def ping():
    return ""

@app.route("/start")
def start():
    t1 = threading.Thread(target=bot.start())
    t1.start()
    return "<p>Bot initiated.</p>"