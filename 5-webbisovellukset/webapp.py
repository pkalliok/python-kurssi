#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello(): return "Dead kittens and suffering"

