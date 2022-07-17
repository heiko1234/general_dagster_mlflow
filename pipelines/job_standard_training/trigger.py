
import os
from dagster import ScheduleEvaluationContext, schedule
from dagster import RunRequest, SkipReason, sensor

from pipelines.general.resources import BlobStorageConnector

from pipelines.job_standard_training.job import (
    job_train_mlflow_models
)

from pipelines.general.utility import (
    read_configuration
)
from pipelines.general.resources import (
    read_yaml_file
)



@schedule(
    job=job_train_mlflow_models,
    cron_schedule="*/2 * * * *", #every 2 min
    pipeline_name="dagster_pipeline"
)
def scheduler_dagster_mlflow_training(context: ScheduleEvaluationContext):

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
                            "subcontainername": general_configuration["subblobcontainer_data"],
                            "filename": general_configuration["filename_data"],
                        }
                    },
                "load_blobyaml":
                    {"inputs":
                        {
                            "containername": general_configuration["blobcontainer"],
                            "subcontainername": general_configuration["subblobcontainer_config"],
                            "filename": general_configuration["filename_config"],
                        }
                    }
            }
    }

    return output



@sensor(
    job=job_train_mlflow_models, 
    minimum_interval_seconds=60
)
def sensor_train_mlflow_model_training(context):

    local_run = os.getenv("LOCAL_RUN", False)
    if local_run:
        general_configuration = read_configuration("./pipelines/job_standard_training/job_mlflow_training_config.yaml")

    else:
        general_configuration = read_yaml_file(
            container_name="sklearn", blob="configuration_data", file="job_mlflow_training_config.yaml"
        )
    
    DataFetcher = BlobStorageConnector(container_name=general_configuration["blobcontainer"])

    data_file = DataFetcher.get_parquet_file(
        subcontainer=general_configuration["subblobcontainer_data"], 
        file=general_configuration["filename_data"]
    )

    data_length = data_file.shape[0]

    last_length = int(context.cursor) if context.cursor else 0

    if data_length == last_length:

        context.updata_cursor(str(data_length))

        yield RunRequest(
            run_key=f"updated_datashape_{data_length}",
            run_config={
                "ops":
                    {"load_blobdata":
                        {"inputs":
                            {
                                "containername": general_configuration["blobcontainer"],
                                "subcontainername": general_configuration["subblobcontainer_data"],
                                "filename": general_configuration["filename_data"],
                            }
                        },
                    "load_blobyaml":
                        {"inputs":
                            {
                                "containername": general_configuration["blobcontainer"],
                                "subcontainername": general_configuration["subblobcontainer_config"],
                                "filename": general_configuration["filename_config"],
                            }
                        }
                    }
            }
        )








