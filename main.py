import pandas as pd
import numpy as np
import emoji
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from uuid import uuid4
import gcsfs
from flask import Flask, redirect, request, url_for, session, jsonify, render_template
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import secrets
import functools
from flask_cors import CORS

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)

# Initialize embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
persist_directory = "faiss_index"
vectordb = FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)
retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 5})

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_report():
    data = request.get_json()
    if 'report' in data:
        report = data['report']
        if report == "":
            return {"error":"Please enter the description of the listnr report"}
        top_list = retriever.invoke(emoji.demojize(report))
        top_5 = [i.metadata["tag"] for i in top_list]

        response = {i + 1: item for i, item in enumerate(top_5)}
    else:
        response = {
            "error": "No 'report' key found in the JSON"
        }, 400  # Bad Request

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
