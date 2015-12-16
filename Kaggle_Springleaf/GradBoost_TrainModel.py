###########################################
##   KAGGLE COMPETITION, SPRINGLEAF	 ##
##            AUTUMN 2015                ##
##       Author: Kimberly Fessel         ##
###########################################


import pandas as pd
import numpy as np
import random
import dill

from sklearn.base             import BaseEstimator, TransformerMixin
from sklearn.preprocessing    import LabelEncoder, LabelBinarizer, Imputer
from sklearn.ensemble         import GradientBoostingClassifier


#-------------------------
#

print( '\nreading the training data' )

random.seed( 23 )

f         = 'Data/train.csv'
num_lines = sum( 1 for l in open(f) )
size      = int( num_lines/1.25 )  #Sample including 80% training data, memory constraints
skip_idx  = random.sample( range(1, num_lines), num_lines - size )
train     = pd.read_csv( f, skiprows=skip_idx )
y         = train.target
train     = train.drop( ['target'], axis=1 )


#-------------------------
#

print( '\nconverting to numerics' )
def convert_to_numerics( df ):

    ##Convert date columns 
    date_cols = [73, 75, 156, 157, 158, 159, \
                 166, 167, 168, 169, 176, 177, 178, 179, 204, 217]
    for j in date_cols:
        le_date    = LabelEncoder()
        df.ix[:,j] = le_date.fit_transform( \
                        pd.to_datetime(df.ix[:,j], format='%d%b%y:%H:%M:%S') \
                        )
                        
    ##Encode object/boolean columns with numeric labels            
    for i in range( len(df.columns) ):
        if df.ix[:,i].dtype == 'object':
            le         = LabelEncoder()
            df.ix[:,i] = le.fit_transform( df.ix[:,i] )
        elif df.ix[:,i].dtype == 'bool':
            lb         = LabelBinarizer()
            df.ix[:,i] = lb.fit_transform( df.ix[:,i] )
    return df

train = convert_to_numerics( train )


#-------------------------
#
class GBmodel( BaseEstimator, TransformerMixin ):
    '''Model steps include:
          1. Impute data to set NAs to median of feature.
          2. Fit gradient boosting model to training data.'''

    def __init__( self ):
        self.imp = Imputer( missing_values='NaN', strategy='median', axis=0 )
        self.gb  = GradientBoostingClassifier( n_estimators=110, \
                                               min_samples_leaf=2 )

    def fit_transform( self, X, y ):
        X = self.imp.fit_transform( X )
        self.gb.fit( X, y )
        return self

    def predict( self, X ):
        X = self.imp.transform( X )
        y = self.gb.predict_proba( X )
        return y[:,1]
        
        
#-------------------------
#
print( '\ntraining model' )   

gb = GBmodel()
gb.fit_transform( train, y )


#-------------------------
#
print( '\nserializing model' )   

with open( 'gbEstimator.pkl', 'w' ) as g:
    dill.dump( gb, g )
