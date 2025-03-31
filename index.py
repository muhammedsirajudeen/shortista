import os
from flask import Flask, render_template,jsonify, request
from pipeline.pipeline import entrypoint
from dotenv import load_dotenv
from load_keys import API_KEY
load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-clip",methods=["POST"])
def generate_clip():
    youtuber_name=request.json.get('youtuber')
    entrypoint(youtuber_name)
    return jsonify({"message":"success"})

if __name__ == "__main__":
    app.run(debug=True)

