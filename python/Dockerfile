FROM ubuntu:16.04

# Install wget and pip3
RUN apt update && \
    apt install -y wget python3-pip

# Install the bucket command wrapper, as well as a number of other useful utilities
RUN pip3 install bucket_command_wrapper==0.2.0 biopython pandas numpy awscli
