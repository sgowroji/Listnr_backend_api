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
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

from flask import Flask, request, jsonify, render_template
fs = gcsfs.GCSFileSystem()

path = "gs://lstnr-reports-data/AIS-feedback - final_reports_till_August24_2025.csv"

df = pd.read_csv(fs.open(path))

df = df.drop(columns=['date', "report_id", "key"])
df.columns = [ "Reports", "Category"]
#drop null values
df.dropna(inplace=True)

#clear the emojis
df['Reports'] = df['Reports'].apply(lambda x: emoji.demojize(x))

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Convert the reports to langchain document
Langchain_Documents = []
for index, row in df.iterrows():
    doc = Document(
    page_content=row["Category"]+ " " +row["Reports"],
    metadata={"tag": row["Category"]},
    id=index,)
    Langchain_Documents.append(doc)

vectordb = FAISS.from_documents(Langchain_Documents, embeddings)
vectordb.save_local("faiss_index")
