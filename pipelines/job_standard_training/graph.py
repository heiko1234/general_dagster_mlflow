
from dagster import graph



@graph
def mlflow_execution_graph():

    df = load_blob_data()

    validate_data(df)

    filtered_df=filtered_data(df)

    train_models(filtered_df)


















