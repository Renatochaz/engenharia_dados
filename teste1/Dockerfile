# Use latest sqlserver docker image
FROM mcr.microsoft.com/mssql/server:2019-latest
USER root

COPY requirements.txt /requirements.txt

# Create sample data

# Update and install system libs
RUN apt-get update -y
RUN apt install python3-pip -y
RUN pip3 install --no-cache-dir --upgrade pip
RUN apt install unixodbc-dev -y
RUN pip3 install --upgrade cython

# Install specific python requirements
RUN pip3 install -r requirements.txt

# Create working directory
ADD . /scripts
WORKDIR /scripts

