import mlflow

def MathCalculate(x,n):
    return x**n


if __name__=="__main__":
    with mlflow.start_run():
        x,n=6,6
        y=MathCalculate(x,n)
        mlflow.log_param("x",x)
        mlflow.log_param("n",n)
        mlflow.log_metric("y",y)
