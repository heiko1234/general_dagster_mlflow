
from dagster import ScheduleEvaluationContext, schedule

from pipelines.job_standard_training.job import (
    job_train_mlflow_models
)

from pipelines.general.utility import (
    read_configuration
)

general_configuration = read_configuration("./pipelines/job_standard_training/job_mlflow_training_config.yaml")



@schedule(
    job=job_train_mlflow_models,
    cron_schedule="*/2 * * * *", #every 2 min
    pipeline_name=general_configuration["pipeline_name"]
)
def trigger_dagster_mlflow_training(context: ScheduleEvaluationContext):
    output = {
        "ops":
            {
                
            }
    }










