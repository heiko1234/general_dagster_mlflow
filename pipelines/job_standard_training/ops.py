
from dagster import op
from dagster import In, Out

import pandas as pd
import yaml

from pipelines.general.resources import (
    read_parquet_file,
    read_yaml_file
)


@op
def check_data_quality(data: pd.DataFrame):
    """Any data quality check

    Args:
        data (pd.DataFrame): a pandas DataFrame
    """

    return True


@op
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
    return df



@op
def load_blobyaml(context, containername, subcontainername, filename):

    context.log.info(f"containername: {containername}")
    context.log.info(f"subcontainername: {subcontainername}")
    context.log.info(f"filename: {filename}")

    file_name = filename.split(".")[0]
    file_type = filename.split(".")[1]

    context.log.info(f"file_name: {file_name}")
    context.log.info(f"file_type: {file_type}")

    configuration = read_yaml_file(container_name=containername, blob=subcontainername, file=filename)
    return configuration




@op
def filtered_data(context, dataframe, configuration):

    output_df = dataframe

    return output_df


@op
def mlflow_training_run(context, dataframe, configuration):
    
    print("Not yet done :) ")



