FROM apache/airflow:latest-python3.12

COPY requirements.txt /
RUN pip3 install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

# Libs necessárias para o MSSQL Server
# COPY ./libodbc.so.2 /var/lib64/libodbc.so.2
# COPY ./pyodbc.so /var/lib64/pyodbc.so

USER root

# Instala o suporte ao MSSQL 
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
&& curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list \
&& apt-get update \
&& ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
&& pip3 install apache-airflow-providers-microsoft-mssql[common.sql]

# Instala o suporte ao PostgreSQL
RUN pip3 install apache-airflow-providers-postgres

# # Instala o suporte ao MySQL
# RUN pip3 install apache-airflow-providers-mysql

# # Instala o suporte ao Databricks
# RUN pip3 install apache-airflow-providers-databricks

# # Instala o suporte ao Snowflake
# RUN pip3 install apache-airflow-providers-snowflake[common.compat]

# # Instala o suporte ao BOTO3 (AWS)
RUN pip3 install apache-airflow-providers-amazon

# # Instala o suporte a Azure
# RUN pip3 install apache-airflow-providers-microsoft-azure

# # Instala o suporte ao Google (GCP, Ads, Firebase, LevelDB, Workspace, Marketing Platform)
# RUN pip3 install apache-airflow-providers-google

# Instala o suporte ao Slack
RUN pip3 install apache-airflow-providers-slack

# Instala o suporte ao dag factory
RUN pip3 install dag-factory

USER airflow