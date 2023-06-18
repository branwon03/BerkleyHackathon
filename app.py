from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

queries = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'submit_item' in request.form:
            item = request.form.get('item')
            queries.append(item)
        elif 'submit_all' in request.form:
            #run the API method
            print("here")
        elif 'pdf' in request.files:
            pdf_file = request.files['pdf']
            if pdf_file.filename != '':
                filename = secure_filename(pdf_file.filename)
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    
    return render_template('index.html', grocery_list=queries)

if __name__ == '__main__':
    app.run()