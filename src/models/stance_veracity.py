from sklearn.base import BaseEstimator

import numpy as np
#from sklearn import tree
from sklearn import svm
from sklearn.linear_model import LogisticRegression

class two_step(BaseEstimator):
    """ Draft of two step classifier """
    def __init__(self, stance_model, veracity_model):#, comment_model, other_model):
        self.stance_model = stance_model
        self.veracity_model = veracity_model

    '''
    Maybe conversations features
    '''
    def fit(self, X_stances, y_stances, X_verif, y_verif):
        self.stance_model.fit(X_stances,y_stances)

        #Train model 2 to guess others (SDQ)
        self.veracity_model.fit(X_verif,y_verif)

        return self

    def predict(self, X):
        #Get all comment predictions
        comment_pred = self.m1.predict(X)

        # for each which is predicted as not comment (0), store it and its original idx
        non_comments = []
        for i in range(len(comment_pred)):
            if comment_pred[i] == 0:
                non_comments.append((i, X[i]))
            else:
                comment_pred[i] = 3 #set to proper value

        # predict others
        other_pred = self.m2.predict([x[1] for x in non_comments])

        # insert predictions from model two into 0 preds from m1
        for (idx, pred) in enumerate(other_pred):
            org_idx = non_comments[idx][0] # original idx in list
            comment_pred[org_idx] = pred

        #return
        return np.array(comment_pred)

    #def score()