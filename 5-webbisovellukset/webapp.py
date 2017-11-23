#!/usr/bin/env python3

from flask import Flask, redirect
app = Flask(__name__)

@app.route("/")
def root(): return redirect("/hello", code=302)

@app.route("/hello")
def hello(): return "Dead kittens and suffering"

