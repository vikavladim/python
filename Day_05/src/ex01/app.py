import os
from logging import warning

from flask import Flask, render_template, request, send_from_directory, jsonify

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    warning = ''
    if request.method == 'POST' and request.files['file']:
        f = request.files['file']
        if allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        else:
            warning = 'Non-audio file detected'

    return render_template('index.html', audiofiles=find_audio(), warning=warning)

@app.route("/files", methods=['GET'])
def list_files():
    return jsonify(find_audio())

def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in {'mp3', 'ogg', 'wav'}

def find_audio():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return [file for file in files if allowed_file(file)]

if __name__ == '__main__':
    app.run(debug=True, port=8888)
