# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename
import predict

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd() , 'cache')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>RankFace</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Submit>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predict.save_predict_img(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                  os.path.join(app.config['UPLOAD_FOLDER'], '#' + filename))
            file_url = url_for('uploaded_file', filename='#' + filename)
            return '<br><img src=' + file_url + '>'
    return html


if __name__ == '__main__':
    for file in os.listdir('./cache'):
        os.remove(os.path.join('./cache', file))
    app.run(host='0.0.0.0', port=5000)
    # print os.path.join(os.getcwd() , 'cache')
