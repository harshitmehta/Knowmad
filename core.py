# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 01:56:55 2017

@author: HARSHIT
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score




def predict():
    #to_predict = user_data
    df = pd.read_csv('survey.csv')
    df.drop(df.columns[[0, 4, 5, 26]], axis=1, inplace=True)
    # Deleting Timestamp, State, self-employed and comments

    df['Gender'] = df['Gender'].str.lower()

    df.Gender = df.Gender = df.Gender.replace('m', 'male')
    df.Gender = df.Gender = df.Gender.replace('male-ish', 'male')
    df.Gender = df.Gender = df.Gender.replace('maile', 'male')
    df.Gender = df.Gender = df.Gender.replace('mal', 'male')
    df.Gender = df.Gender = df.Gender.replace('male (cis)', 'male')
    df.Gender = df.Gender = df.Gender.replace('make', 'male')
    df.Gender = df.Gender = df.Gender.replace('man', 'male')
    df.Gender = df.Gender = df.Gender.replace('msle', 'male')
    df.Gender = df.Gender = df.Gender.replace('mail', 'male')
    df.Gender = df.Gender = df.Gender.replace('malr', 'male')
    df.Gender = df.Gender = df.Gender.replace('cis man', 'male')
    df.Gender = df.Gender = df.Gender.replace('cis male', 'male')
    df.Gender = df.Gender = df.Gender.replace('male', 'male')
    df.Gender = df.Gender = df.Gender.replace('male ', 'male')

    df.Gender = df.Gender.replace('f', 'female')
    df.Gender = df.Gender.replace('cis female', 'female')
    df.Gender = df.Gender.replace('woman', 'female')
    df.Gender = df.Gender.replace('femake', 'female')
    df.Gender = df.Gender.replace('female ', 'female')
    df.Gender = df.Gender.replace('cis-female/femme', 'female')
    df.Gender = df.Gender.replace('female (cis)', 'female')
    df.Gender = df.Gender.replace('femail', 'female')

    df.Gender = df.Gender.replace('trans-female', 'trans')
    df.Gender = df.Gender.replace('something kinda male?', 'trans')
    df.Gender = df.Gender.replace('queer/she/they', 'trans')
    df.Gender = df.Gender.replace('non-binary', 'trans')
    df.Gender = df.Gender.replace('nah', 'trans')
    df.Gender = df.Gender.replace('all', 'trans')
    df.Gender = df.Gender.replace('enby', 'trans')
    df.Gender = df.Gender.replace('fluid', 'trans')
    df.Gender = df.Gender.replace('genderqueer', 'trans')
    df.Gender = df.Gender.replace('androgyne', 'trans')
    df.Gender = df.Gender.replace('agender', 'trans')
    df.Gender = df.Gender.replace('male leaning androgynous', 'trans')
    df.Gender = df.Gender.replace('guy (-ish) ^_^', 'trans')
    df.Gender = df.Gender.replace('trans woman', 'trans')
    df.Gender = df.Gender.replace('neuter', 'trans')
    df.Gender = df.Gender.replace('female (trans)', 'trans')
    df.Gender = df.Gender.replace('queer', 'trans')
    df.Gender = df.Gender.replace('ostensibly male, unsure what that really means', 'trans')
    df.Gender = df.Gender.replace('p', 'trans')
    df.Gender = df.Gender.replace('a little about you', 'trans')

    

    df['Age'] = pd.to_numeric(df['Age'],errors='coerce')
    def age_process(age):
        if age>=0 and age<=100:
            return age
        else:
            return np.nan
    df['Age'] = df['Age'].apply(age_process)

    df = df.dropna(subset=['work_interfere'])
    df = df.dropna(subset=['Age'])
    df.copy = df

    # convert binary columns to 0 and 1
    for col in df.select_dtypes(include=['object']):
        u_count = len(df[col].unique()) 
        if u_count == 2:
            first = list(df[col].unique())[-1]
            df[col] = (df[col] == first).astype(int)
            print('converted', col)


    df.work_interfere = df.work_interfere.map({'Never': 0, 'Rarely': 1,'Sometimes': 2, 'Often': 3})

    df.no_employees = df.no_employees.map({'6-25': 6, '26-100': 26,'100-500': 100, '500-1000': 500, 'More than 1000': 1000, '1-5': 
                                           1})

    mapping = {'Yes': 1, 'No': -1, "Don't know": 0,'Not sure': 0, 'Maybe': 0, 'Some of them': 0}
    three_factor = {'Yes': 1, 'No': -1, 'Not sure': 0}
    for col in df.select_dtypes(include=['object']):
        uniques = set(df[col].unique())
        if (uniques == {'Yes', 'No', "Don't know"} or
            uniques == {'Yes', 'No', 'Not sure'} or
            uniques == {'Yes', 'No', 'Maybe'} or
            uniques == {'Yes', 'No', 'Some of them'}):
            print('converted', col, 'To -1, 0, 1')
            df[col] = df[col].map(mapping)

    df.leave = df.leave.map({'Very easy': 0, 'Somewhat easy': 1, "Don't know": 2, 'Somewhat difficult': 3,
                             'Very difficult': 4
                            })

    df.Gender = df.Gender.map({'male': 1, 'female': -1,
                                               'trans': 0})

    del df['Country']

    key_mask = np.random.rand(len(df)) < 0.8

    train = df[key_mask]

    test = df[~key_mask]

    x, y = train.drop('treatment', axis=1), train.treatment

    model = RandomForestClassifier(n_jobs=-1, n_estimators=200, class_weight='balanced')
    scores = cross_val_score(model, x, y, scoring='roc_auc', cv=5)
    print(scores.mean())

    model.fit(x,y)

    #importances = model.feature_importances_
    #std = np.std([tree.feature_importances_ for tree in model.estimators_],
    #             axis=0)
    #indices = np.argsort(importances)[::-1]

    #print("Feature ranking:")

    #for f in range(x.shape[1]):
    #    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))


    # feature importance of the model
    #plt.figure()
    #plt.title("Importance of features")
    #plt.bar(range(x.shape[1]), importances[indices],
    #         yerr=std[indices], align="center")
    #plt.xticks(range(x.shape[1]), indices)
    #plt.xlim([-1, x.shape[1]])
    #plt.show()

    #x_test, y_test = test.drop('treatment', axis=1), test.treatment

    #Predict Output
    #predicted= model.predict(to_predict)
    #return predicted

    #pd.crosstab(test['treatment'], predicted)

    #Accuracy Score

    #test_values = y_test.as_matrix()
    #accuracy_score(predicted, test_values)

