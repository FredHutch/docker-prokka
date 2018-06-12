FROM ubuntu:16.04

# Install wget and pip3
RUN apt update && \
    apt install -y wget python3-pip awscli

# Install the bucket command wrapper
RUN pip3 install bucket_command_wrapper==0.2.0

# Install the SRA toolkit
RUN cd /usr/local/bin && \
    wget -q https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2/sratoolkit.2.8.2-ubuntu64.tar.gz && \
    tar xzf sratoolkit.2.8.2-ubuntu64.tar.gz && \
    ln -s /usr/local/bin/sratoolkit.2.8.2-ubuntu64/bin/* /usr/local/bin/ && \
    rm sratoolkit.2.8.2-ubuntu64.tar.gz

# Install finch-rs
RUN mkdir /bin/finch-rs && \
    cd /bin/finch-rs && \
    wget https://github.com/onecodex/finch-rs/releases/download/v0.1.5/finch-linux64-v0.1.5.tar.gz && \
    tar xzvf finch-linux64-v0.1.5.tar.gz && \
    mv finch-linux64-v0.1.5/finch /usr/local/bin/ && \
    rm finch-linux64-v0.1.5.tar.gz && \
    finch -h
