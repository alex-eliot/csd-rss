import threading
from flask import Flask
import bot

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<p>sup</p>"

@app.route("/ping", methods=["GET"])
def ping():
    return ""

@app.route("/start", methods=["GET"])
def start():
    t1 = threading.Thread(target=bot.start())
    t1.start()
    t1.join()
    return "<p>Bot initiated.</p>"