#!/usr/bin/env python3

from flask import Flask, redirect, jsonify
app = Flask(__name__)

@app.route("/")
def root(): return redirect("/hello", code=302)

@app.route("/ping")
def ping(): return "pong"

@app.route("/hello")
def hello(): return "Dead kittens and suffering"

todos = []

@app.route("/api/v1/todo")
def list_todos(): return jsonify(todos)

