#!/usr/bin/env python3

from flask import Flask, redirect, jsonify, request
app = Flask(__name__)

@app.route("/")
def root(): return redirect("/hello", code=302)

@app.route("/ping")
def ping(): return "pong"

@app.route("/hello")
def hello(): return "Dead kittens and suffering"

todos = []

@app.route("/api/v1/todo", methods=['GET'])
def list_todos(): return jsonify(todos)

@app.route("/api/v1/todo", methods=['POST'])
def add_todo():
    todos.append(request.json)
    return jsonify("ok"), 201

