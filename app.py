from flask import Flask, render_template, session, redirect, request, url_for, jsonify, send_file
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import random
import time
import pandas as pd
from pridect import Pridect
from train import Train

app = Flask(__name__)
app.secret_key = "343434343434343"
Bootstrap(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if session.get('model') is None:
        session['model'] = 'dtree'
    return render_template('index.html')


# Function upload dataset image when click poup process
@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('files[]')
    success = False
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join('static', 'data')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        success = True
    if success:
        data_test = pd.read_csv(os.path.join('static', 'data', filename))
        data_test.drop('status_id', axis=1, inplace=True)
        session['filename'] = filename
        return jsonify(result=render_template('list_data.html', data=data_test))


@app.route('/predictdata', methods=['GET', 'POST'])
def predictdata():
    # print(session['filename'])
    result = Pridect().dataPredicted(session['filename'])
    # print(result)
    # return jsonify('aaa')
    persondata = pd.read_csv(os.path.join('static', 'data', session['filename']))
    return jsonify(result=render_template('predicted_data.html', data=persondata, result=result))


@app.route('/train', methods=['POST', 'GET'])
def train():
    return render_template('train.html')


# Function upload dataset image when click poup process
@app.route('/uploadfiletrain', methods=['GET', 'POST'])
def uploadfiletrain():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('files[]')
    success = False
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join('static', 'data')
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))
        success = True
    if success:
        session['filename_train'] = filename
        return jsonify(result='Done upload')


@app.route('/traindata', methods=['GET', 'POST'])
def traindata():
    print(session['filename_train'])
    result = Train().dataTrain(session['filename_train'])
    # print(result)
    return jsonify(result='<div align="center"><img src="/static/default/done.jpg" style="width: 500px"></div>')


@app.route('/setting', methods=['POST', 'GET'])
def setting():
    if request.form.get('model'):
        session['model'] = request.form.get('model')
    return render_template('setting.html', model=session['model']);


@app.route('/downloadresult')  # this is a job for GET, not POST
def downloadresult():
    return send_file(os.path.join('static', 'result', session.get('result_name')),
                     mimetype='text/csv',
                     attachment_filename=session.get('result_name'),
                     as_attachment=True)


if __name__ == '__main__':
    #app.run(host="192.168.100.247", port="3456")
    app.run()
