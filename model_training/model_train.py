
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV
from sklearn import linear_model
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score, mean_squared_error
import argparse
import pandas as pd
import numpy as np
import pickle

def model_training(args):
    df_test = pd.read_csv(args.test)
    target = pd.read_csv(args.target)
    features_norm = np.load(args.features_path, allow_pickle=True)
    df_test_dict = df_test.to_dict(orient='records')
    rf = RandomForestRegressor(random_state=2)
    final_model = rf.fit(features_norm, target)

    with open(args.dv_path, 'rb') as f_in1:
        dv = pickle.load(f_in1)
    with open(args.scaler_path, 'rb') as f_in2:
        scaler = pickle.load(f_in2)

    test_encoded = dv.transform(df_test_dict)
    test_transformed = pd.DataFrame(test_encoded, columns=dv.feature_names_)
    test_norm = scaler.transform(test_transformed)
    predicted = final_model.predict(test_norm)
    df_predicted = pd.Series(predicted)
    RSME_score = mean_squared_error(y_true=df_test['total_points'], y_pred=predicted, squared=False) #squared=False will RMSE instead of MSE
    R2_score = r2_score(df_test['total_points'], predicted)

    print('RMSE:', RSME_score)
    print('R-Squared:', R2_score)
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--features_path')
    parser.add_argument('--target')
    parser.add_argument('--test')
    parser.add_argument('--dv_path')
    parser.add_argument('--scaler_path')
    args = parser.parse_args()
    model_training(args) 
