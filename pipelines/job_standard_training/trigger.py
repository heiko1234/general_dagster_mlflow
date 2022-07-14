
import os
from dagster import ScheduleEvaluationContext, schedule

from pipelines.job_standard_training.job import (
    job_train_mlflow_models
)

from pipelines.general.utility import (
    read_configuration
)
from pipelines.general.resources import (
    read_yaml_file
)



# general_configuration["blobcontainer"]
# general_configuration["subblobcontainer"]
# general_configuration["filename"]
# general_configuration




@schedule(
    job=job_train_mlflow_models,
    cron_schedule="*/2 * * * *", #every 2 min
    pipeline_name="dagster_pipeline"
)
def trigger_dagster_mlflow_training(context: ScheduleEvaluationContext):

    local_run = os.getenv("LOCAL_RUN", False)
    if local_run:
        general_configuration = read_configuration("./pipelines/job_standard_training/job_mlflow_training_config.yaml")

    else:
        general_configuration = read_yaml_file(
            container_name="coinbasedata", blob="configuration_data", file="job_mlflow_training_config.yaml"
        )
    output = {
        "ops":
            {
                "load_blobdata":
                    {"inputs":
                        {
                            "containername": general_configuration["blobcontainer"],
                            "subcontainername": general_configuration["subblobcontainer"],
                            "filename": general_configuration["filename"],
                        }
                    },
                "load_blobyaml":
                    {"inputs":
                        {
                            "containername": general_configuration["blobcontainer"],
                            "subcontainername": general_configuration["subblobcontainer"],
                            "filename": "job_mlflow_training_config.yaml",
                        }
                    }
            }
    }

    return output










