

from dagster import repository

from pipelines.job_standard_training.job import (
    job_train_mlflow_models
)
from pipelines.job_standard_training.trigger import (
    trigger_dagster_mlflow_training
)


@repository
def data_pipeline():
    """Dagster repository to run pipelines for project"""


    return [
        job_train_mlflow_models,
        trigger_dagster_mlflow_training

    ]


