
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
import argparse
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os
import pickle
import numpy as np

def data_encoding(args):
    df_allseasons_final = pd.read_csv(args.train)
    df_allseasons_final.set_index('year', inplace=True)
    # Sort index (just in case).
    df_allseasons_final.sort_index(inplace=True)
    # Assign features and target variable.
    features = df_allseasons_final.drop(['total_points'], axis = 1)
    # target = df_allseasons_final['total_points']

    # Convert dataframe to a dictionary.
    features_dict = features.to_dict(orient='records')

    dv_final = DictVectorizer(sparse=False) 

    # sparse = False makes the output is not a sparse matrix.

    features_encoded = dv_final.fit_transform(features_dict)
    vocab_final = dv_final.vocabulary_
    features_transformed = pd.DataFrame(features_encoded, columns=dv_final.feature_names_)
    # Normalizing the train data.
    min_max_scaler_final = MinMaxScaler()

    # Fit scalar and transform train data.
    features_norm = min_max_scaler_final.fit_transform(features_transformed)

    data_path = './data_encoding/preprocessed_data'
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    np.save(f'{data_path}/features.npy', features_norm)

    if not os.path.exists('./model'):
        os.makedirs('./model')

    with open('./model/dv', 'wb') as f_out2:
        pickle.dump(dv_final, f_out2)

    with open('./model/min_max_scaler', 'wb') as f_out3:
        pickle.dump(min_max_scaler_final, f_out3)

    df_allseasons_final.to_csv('target.csv')

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train')
    args = parser.parse_args()
    data_encoding(args) 
