FROM ubuntu:16.04

# Install wget and pip/pip3
RUN apt update && \
    apt install -y wget python-pip python3-pip

# Install the bucket command wrapper
RUN pip3 install bucket_command_wrapper==0.2.0

# Install fastqp
RUN pip install fastqp matplotlib==2.0.0
