import os
import numpy as np
import pandas as pd
import argparse

from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse

import mlflow
import mlflow.sklearn 


def get_data():
    URL="http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    try:
        data=pd.read_csv(URL,sep=";")
        return data
    
    except Exception as e:
        raise e

def evaluate(y_test,pred):
    rmse=np.sqrt(mean_squared_error(y_test,pred))
    mae=mean_absolute_error(y_test,pred)
    r2=r2_score(y_test,pred)

    return rmse,mae,r2

def main(alpha,l1_ratio):
    df=get_data()
    x=df.drop('quality',axis=1)
    y=df.quality

    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=123)
    with mlflow.start_run():

        lr=ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=42)
        lr.fit(x_train,y_train)
        pred=lr.predict(x_test)

        rmse,mae,r2=evaluate(y_test,pred)
        
        print(f'elasticnet parameter : alpha:{alpha} , l1_ratio:{l1_ratio}')
        print(f'elasticnet metrics : rmse:{rmse} , mae:{mae},r2:{r2}')
        mlflow.log_param("alpha",alpha)
        mlflow.log_param("l1_ratio",l1_ratio)

        mlflow.log_metric("rmse",rmse)
        mlflow.log_metric("mae",mae)
        mlflow.log_metric("r2",r2)



if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--alpha","-a",type=float,default=0.5)
    args.add_argument("--l1_ratio","-l1",type=float,default=0.5)
    parsed_args=args.parse_args()
    try:
        main(alpha=parsed_args.alpha,l1_ratio=parsed_args.l1_ratio)
    except Exception as e:
        raise e
