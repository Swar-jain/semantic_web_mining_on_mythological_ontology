from flask import Flask
import load_data
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello Idhant."

@app.route('/character/<character>')
def show_dropdown_list(character):
    return load_data.form_query(character)