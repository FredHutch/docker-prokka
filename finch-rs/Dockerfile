FROM ubuntu:16.04

# Install wget and pip3
RUN apt update && \
    apt install -y wget python3-pip

# Install the bucket command wrapper
RUN pip3 install bucket_command_wrapper==0.2.0

# Install finch-rs
RUN mkdir /bin/finch-rs && \
    cd /bin/finch-rs && \
    wget https://github.com/onecodex/finch-rs/releases/download/v0.1.5/finch-linux64-v0.1.5.tar.gz && \
    tar xzvf finch-linux64-v0.1.5.tar.gz && \
    mv finch-linux64-v0.1.5/finch /usr/local/bin/ && \
    rm finch-linux64-v0.1.5.tar.gz && \
    finch -h
