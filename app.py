from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, download_loader
import os
os.environ['OPENAI_API_KEY'] = "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"
import logging
import sys
from pathlib import Path
import openai
from markupsafe import Markup



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'
folder_path = './uploads'

openai.api_key = "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"

queries = []

result= ""

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.files)
        if 'submit_item' in request.form:
            item = request.form.get('item')
            queries.append(item)
        elif 'pdf' in request.files:
            print("here")
            
            # empties the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            pdf_file = request.files['pdf']
            if pdf_file.filename != '':
                print("here2")
                filename = secure_filename(pdf_file.filename)
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif 'remove' in request.form:
            item = request.li.get('item')
            print(item)
            queries.remove(item)

    
    
    return render_template('index.html', queries=queries)

@app.route("/remove", methods=['POST'])
def remove() :
    item = request.form.get('item')
    if item in queries:
        queries.remove(item)
    return redirect('/')


@app.route("/submit", methods=['GET'])
def submit() :
        files = os.listdir(folder_path)
        if len(files) == 1:  # Check if there is only one file in the folder
            file_path = os.path.join(folder_path, files[0])
        else:
            print("There is not exactly one file in the folder.")

        PDFReader = download_loader("PDFReader")

        loader = PDFReader()
        documents = loader.load_data(file=Path(file_path))
        print(documents[0].get_text()) # prints the right thing

        index = GPTVectorStoreIndex.from_documents(documents)

        # here we need to change the string based on the queries entered
        # site should error if no queries
        query = "Find the"

        if len(queries) == 1 :
            query = query + queries[0]
        else :
            for i in range(len(queries)):
                if (i == len(queries) - 1) :
                    query = query + " and"
                query = query + " " + queries[i] + ","
        query = query + " in the text. Format the answer with the [keyword]:, followed by the results and a new line"
        print(query)
        response = index.as_query_engine().query(query)
        result = str(response) # convert to a string
        result = result.replace('\n', '<br>')
        return render_template('result.html', result=Markup(result))

if __name__ == '__main__':
    app.run()
