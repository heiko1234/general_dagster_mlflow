
from dagster import op
from dagster import In, Out

import pandas as pd
# import yaml

from pipelines.general.resources import (
    read_parquet_file,
    read_yaml_file
)
# from pipelines.general.utility import (
#     read_configuration
# )
from pipelines.general.mlflow_functions import (
    mlflow_training
)

@op
def check_data_quality(context, data: pd.DataFrame):
    """Any data quality check

    Args:
        data (pd.DataFrame): a pandas DataFrame
    """

    # https://pandera.readthedocs.io/en/stable/

    context.log.info(f"data: {data.head}")

    return False


@op(ins={"containername": In(dagster_type=str), "subcontainername": In(dagster_type=str), "filename": In(dagster_type=str)})
def load_blobdata(context, containername, subcontainername, filename):

    context.log.info(f"containername: {containername}")
    context.log.info(f"subcontainername: {subcontainername}")
    context.log.info(f"filename: {filename}")

    file_name = filename.split(".")[0]
    file_type = filename.split(".")[1]

    context.log.info(f"file_name: {file_name}")
    context.log.info(f"file_type: {file_type}")

    df = read_parquet_file(
        container_name=containername, 
        blob=subcontainername, 
        file=filename
    )
    context.log.info(f"data: {df.head()}")
    return df



@op(ins={"containername": In(dagster_type=str), "subcontainername": In(dagster_type=str), "filename": In(dagster_type=str)})
def load_blobyaml(context, containername, subcontainername, filename):

    context.log.info(f"containername: {containername}")
    context.log.info(f"subcontainername: {subcontainername}")
    context.log.info(f"filename: {filename}")

    file_name = filename.split(".")[0]
    file_type = filename.split(".")[1]

    context.log.info(f"file_name: {file_name}")
    context.log.info(f"file_type: {file_type}")

    configuration = read_yaml_file(container_name=containername, blob=subcontainername, file=filename)

    context.log.info(f"configuration: {configuration}")
    return configuration




@op
def filtered_data(context, dataframe, configuration):

    context.log.info(f"dataframe: {dataframe.head}")
    context.log.info(f"filter config: {configuration}")

    output_df = dataframe

    context.log.info(f"output_df: {output_df.head}")

    return output_df


@op
def mlflow_training_run(context, dataframe, configuration):
    
    mlflow_training(data=dataframe, configuration=configuration)



