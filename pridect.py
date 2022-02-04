import numpy as np
from flask import Flask, render_template, session, redirect, request, url_for, jsonify
import os
import xlsxwriter
import pandas as pd
import openpyxl
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pickle
from random import randint, randrange


class Pridect(object):
    def __init__(self):
        self.path = os.path.join('static')
        self.path_img = os.path.join('static', 'data')
        self.filename = ''
        self.modelname = 'model_' + session.get('model') + ".h5"

    def dataPredicted(self, filename):
        data_test = pd.read_csv(os.path.join('static', 'data', filename))
        predeteddata = pd.read_csv(os.path.join('static', 'data', filename))
        predeteddata.drop('status_id', axis=1, inplace=True)
        predeteddata.drop('start_date', inplace=True, axis=1)
        predeteddata.drop('acc_number', axis=1, inplace=True)
        predeteddata.drop('vbcode', axis=1, inplace=True)
        # load the model from disk
        loaded_model = pickle.load(open(os.path.join('static', 'model', self.modelname), 'rb'))
        df_output = pd.DataFrame()
        outp = loaded_model.predict(predeteddata).astype(int)
        df_output['id'] = predeteddata.id
        df_output['status_id'] = outp

        # Save Result to CSV
        result_output = pd.DataFrame(data_test)
        result_output['status_id'] = outp
        result_name = "result_" + str(randint(100, 999)) + '.csv'
        session['result_name'] = result_name
        result_output.to_csv(os.path.join('static', 'result', result_name), index=False)

        return df_output
