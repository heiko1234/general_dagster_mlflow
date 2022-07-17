

from dagster import repository

from pipelines.job_standard_training.job import (
    job_train_mlflow_models
)
from pipelines.job_standard_training.trigger import (
    scheduler_dagster_mlflow_training,
    sensor_train_mlflow_model_training
)
# from pipelines.job_standard_training.trigger_sensor import (
#     sensor_train_mlflow_model
# )


@repository
def data_pipeline():
    """Dagster repository to run pipelines for project"""


    return [
        job_train_mlflow_models,
        scheduler_dagster_mlflow_training,
        sensor_train_mlflow_model_training
    ]


