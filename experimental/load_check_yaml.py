





from pipelines.general.resources import (
    BlobStorageConnector,
    read_yaml_file
)


yaml_file = BlobStorageConnector(container_name="sklearn").list_files_in_subcontainer(subcontainer="configuration_data", files_with=".yaml")
yaml_file

yaml_file = read_yaml_file(container_name="sklearn", blob="configuration_data", file = "job_mlflow_training_config.yaml")
yaml_file

