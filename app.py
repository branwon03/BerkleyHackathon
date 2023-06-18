from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
os.environ['OPENAI_API_KEY'] = "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"

import logging
import sys
import requests
from pathlib import Path


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index import GPTVectorStoreIndex, download_loader

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'

queries = []

result= ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.files)
        if 'submit_item' in request.form:
            item = request.form.get('item')
            queries.append(item)
        elif 'pdf' in request.files:
            print("here")
            # pdf goes away when rendered again
            pdf_file = request.files['pdf']
            if pdf_file.filename != '':
                print("here2")
                filename = secure_filename(pdf_file.filename)
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    
    return render_template('index.html', queries=queries)

@app.route("/submit", methods=['GET'])
def submit() :
    result = "here"
    return "here"

if __name__ == '__main__':
    app.run()


    # PDFReader = download_loader("PDFReader")
    # loader = PDFReader()
    # documents = loader.load_data(file=Path('./uploads/reference.pdf')) 
    # print("get here")

    # index = GPTVectorStoreIndex.from_documents(documents)
    # query_engine = index.as_query_engine()
    # print("get here2")

    # # here we need to change the string based on the queries entered
    # # site should error if no queries
    # query = "What is the"

    # for i in range(len(queries)):
    #     if (i == len(queries) - 1) :
    #         query = query + " and"
    #     query = query + " " + queries[i]
    # query = query + " in the text"
    # print("get here3") 
    # response = query_engine.query(query)
    # result = response
    # print("get here4")
    # return render_template('result.html', result=result)