###########################################
##  KAGGLE COMPETITION, YUMMLY Cooking   ##
##            AUTUMN 2015                ##
###########################################


import simplejson as json
import pandas     as pd
import numpy      as np
import re

from sklearn import metrics
from sklearn import svm

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import BaseEstimator 
from sklearn.grid_search import GridSearchCV

#--------------------------------------------

#Convert json files to data frames
def json_to_df( json_file ):
    mylist = []
    with open( json_file, 'r' ) as f:
        str = ''
        for line in f:
            m = re.search( '(})', line )
            if m:
                str = str + m.group(1)
                mylist.append( json.loads( str ) )
                str = ''
            else:
                str = str + line
    return pd.DataFrame( mylist )

#Process list of ingredients into string prior to feature extraction
def make_text( ser ):
    list_nospaces = ser.apply( lambda y: [x.replace(' ', '') for x in y] )
    my_str        = list_nospaces.apply( lambda x: ','.join(x) )
    return my_str

#Classification Model
class SVCModel( BaseEstimator ):
    '''Model steps include:
          1. Fit CountVectorizer to ingredients data.
          2. Fit SVM (RBF kernel) model to training data.'''
        
    def __init__( self, kernel='rbf', gamma=0.1 ):
        self.kernel = kernel   
        self.gamma = gamma
 
    def fit( self, X, y ):
        self.svc = svm.SVC( kernel=self.kernel, gamma=self.gamma )
        self.vec = CountVectorizer()
        V = self.vec.fit_transform( X )
        self.svc.fit( V, y )    
    
    def predict( self, X ):
        V = self.vec.transform( X )
        return self.svc.predict( V )
    
#-------------------------------------------- 

svc = SVCModel( )

train = json_to_df( 'train.json' )
test  = json_to_df( 'test.json'  )
 
train_text = make_text( train.ingredients )
test_text  = make_text( test.ingredients )
 
print('training model\n')
svc.fit( train_text, train.cuisine )
 
print('making predictions\n')
ypred = svc.predict( test_text )
 
submit_df = pd.DataFrame( test.id )
submit_df['cuisine'] = ypred
 
g = 'Submissions/svc.csv'
submit_df.to_csv( g, index=False )


#----------------------------------------

##Cross-validation for parameters

#svc = SVCModel()
#train = json_to_df( 'train.json' ) 
#train_text = make_text( train.ingredients )

#parameters={'kernel':['rbf', 'linear', 'poly', 'sigmoid'], 'gamma':[0.05, 0.1, 0.15]}
#gs = GridSearchCV(svc, parameters, scoring='accuracy')  
#gs.fit(train_text, train.cuisine)
#print gs.grid_scores_ 
#print gs.best_params_

