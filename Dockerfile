# Base Airflow image
FROM apache/airflow:2.7.1-python3.9

# Switch to root to install system dependencies
USER root

# Install OS-level packages (compiler, Python headers)
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy local files into container
COPY requirements.txt /opt/airflow/requirements.txt
COPY dags /opt/airflow/dags
COPY pipelines /opt/airflow/pipelines

# Set the Python path so custom code is recognized by Airflow
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

# Switch back to airflow user
USER airflow

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /opt/airflow/requirements.txt

