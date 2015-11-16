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

with open( 'gbEstimator_110.pkl', 'r' ) as f:
    gb = dill.load( f )
    

def convert_to_numerics( df ):

    #Convert date columns
    date_cols = [73, 75, 156, 157, 158, 159, \
                 166, 167, 168, 169, 176, 177, 178, 179, 204, 217]
    for j in date_cols:
        le_date    = LabelEncoder()
        df.ix[:,j] = le_date.fit_transform(            \
                            pd.to_datetime(df.ix[:,j], \
                            format='%d%b%y:%H:%M:%S')  \
                            )
    
    #Convert object/boolean columns to numerics
    for i in range( len(df.columns) ):
        if df.ix[:,i].dtype == 'object':
            le         = LabelEncoder()
            df.ix[:,i]   = le.fit_transform( df.ix[:,i] )
        elif df.ix[:,i].dtype == 'bool':
            lb         = LabelBinarizer()
            df.ix[:,i]   = lb.fit_transform( df.ix[:,i])
    return df


#--------------
# 

print( '\nmaking predictions' )   #Make predicitons in batches

with open( 'Data/submission_gradBoost_serialized_110.csv', 'w' ) as g:
    g.write( 'ID,target\n' )
g.close()
    
reader = pd.read_csv( 'Data/test.csv', chunksize=10000 )
for chunk in reader:
    test             = convert_to_numerics( chunk )
    y_pred           = gb.predict( test )
    submit           = pd.DataFrame( test.ID, columns=['ID'] )
    submit['target'] = y_pred

    with open( 'Data/submission_gradBoost_serialized_110.csv', 'a' ) as g:
        submit.to_csv( g, header=False, index=False )
    g.close()
