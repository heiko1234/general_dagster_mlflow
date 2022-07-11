
from dagster import graph

from pipelines.job_standard_training.ops import (
    mlflow_training_run,
    filtered_data,
    load_blobdata,
    load_blobyaml,
    check_data_quality
)




@graph
def mlflow_execution_graph():

    df = load_blobdata()

    run_config = load_blobyaml()

    check_data_quality(df)

    filtered_df=filtered_data(dataframe=df, configuration=run_config)

    mlflow_training_run(dataframe=filtered_df, configuration=run_config)


















