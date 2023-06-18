from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

grocery_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item = request.form.get('item')
        grocery_list.append(item)
    if 'pdf' in request.files:
            pdf_file = request.files['pdf']
            if pdf_file.filename != '':
                filename = secure_filename(pdf_file.filename)
                pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template('index.html', grocery_list=grocery_list)

if __name__ == '__main__':
    app.run()