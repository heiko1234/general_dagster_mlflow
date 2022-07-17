ARG PYTHON_VERSION=3.8
FROM python:$(PYTHON_VERSION) AS foundation

RUN apt-get update && \
    apt-get install -y build-essential curl wget cmake && \
    apt-get clean && run -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN mkdir -p /opt/dagster/repo
RUN mkdir -p /opt/dagster/repo/data

COPY pipelines/ /opt/dagster/repo/pipelines/

# an extra for the packages
# COPY extra_packages/ /opt/dagster/repo/extra_packages

# copy of data not neccessary, due data download from blob
# COPY data/ /opt/dagster/repo/data

COPY pyproject.toml poetry.toml poetry.lock /opt/dagster/repo/


# How to add ARGs and ENVs
# ARG PYPI_URL
# ENV PYPI_URL=$PYPI_URL


WORKDIR /opt/dagster/repo/

RUN pip install poetry wheel && \
    poetry install --no-dev

# https://github.com/grpc-ecosystem/grpc-health-probe
RUN GRPC_HEATH_PROBE_VERSION=v0.4.0 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64


FROM python:$(PYTHON_VERSION)-slim
COPY --from=foundation /opt/dagster/repo /opt/dagster/repo
COPY --from=foundation /bin/grpc_health_probe /bin/grpc_health_probe
ENV PATH=/opt/dagster/repo/.venv/bin:$PATH
RUN chmod +x /bin/grpc_health_probe

ENV PYTHONUNBUFFERED 1
WORKDIR /opt/dagster/repo

# could be executed via helm values ;)
CMD ["dagster", "api", "grpc", "--module-name", "pipelines.repository", "--host", "0.0.0.0", "--port", "3030"]


