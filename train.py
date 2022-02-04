import numpy as np
import os
import xlsxwriter
from flask import Flask, render_template, session, redirect, request, url_for, jsonify
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
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


class Train(object):
    def __init__(self):
        self.path = os.path.join('static')
        self.path_img = os.path.join('static', 'data')
        self.train_model_name = 'model_' + session.get('model') + ".h5"

    def dataTrain(self, train_filename):
        train = pd.read_csv(os.path.join('static', 'data', train_filename))
        Loan_status = train.status_id
        train.drop('status_id', axis=1, inplace=True)
        """test = pd.read_csv(os.path.join('static', 'data', test_filename))
        test.drop('status_id', axis=1, inplace=True)
        Loan_ID = test.id
        data = train.append(test)"""
        data = train
        data.drop('start_date', inplace=True, axis=1)
        data.drop('acc_number', axis=1, inplace=True)
        data.drop('vbcode', axis=1, inplace=True)

        train_X = data.iloc[:train['id'].count(), ]
        train_y = Loan_status
        # X_test = data.iloc[train['id'].count():, ]
        seed = 5
        train_X, test_X, train_y, test_y = train_test_split(train_X, train_y, random_state=seed)
        if session.get('model') == 'dtree':
            model = DecisionTreeClassifier()
        else:
            model = KNeighborsClassifier()
        model.fit(train_X, train_y)
        # save the model to disk
        filename = os.path.join('static', 'model', self.train_model_name)
        pickle.dump(model, open(filename, 'wb'))
