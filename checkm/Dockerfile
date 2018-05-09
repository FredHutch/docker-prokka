FROM quay.io/fhcrc-microbiome/pplacer:pplacer-v1.1.alpha19--0

RUN pip install checkm-genome

# Install HMMer
RUN mkdir /usr/bin/hmmer && cd /usr/bin/hmmer && \
    wget http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2-linux-intel-x86_64.tar.gz && \
    tar xzvf hmmer-3.1b2-linux-intel-x86_64.tar.gz && rm hmmer-3.1b2-linux-intel-x86_64.tar.gz && \
    mv hmmer-3.1b2-linux-intel-x86_64/binaries/* /usr/local/bin/ && \
    hmmsearch -h

# Install prodigal
RUN cd /usr/local/bin && \
    wget https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux && \
    mv prodigal.linux prodigal && \
    chmod +x prodigal

# Install the checkm database
RUN mkdir /usr/local/checkm && \
    cd /usr/local/checkm && \
    wget https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz && \
    tar xzvf checkm_data_2015_01_16.tar.gz

# The next line is disgusting, please avert your gaze. Checkm does not behave as documented.
RUN echo "/usr/local/checkm/" | checkm data setRoot || true

RUN checkm -h