

from pipelines.job_standard_training.graph import (
    mlflow_execution_graph
)


job_train_mlflow_models = mlflow_execution_graph.to_job(
    name="mlflow_training", 
    resource_defs={}
)
