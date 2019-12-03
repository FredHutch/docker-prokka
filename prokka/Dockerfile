FROM ummidock/prokka:1.12

RUN apt-get update
RUN apt-get install -y curl git python3-pip

RUN pip3 install bucket_command_wrapper==0.2.0

# Install tbl2asn
RUN cd /bin && \
    wget --quiet ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/tbl2asn/linux64.tbl2asn.gz && \
    gunzip linux64.tbl2asn.gz && \
    mv linux64.tbl2asn tbl2asn && \
    chmod +x tbl2asn && \
    tbl2asn --help >/dev/null


# Install barrnap
RUN cd /usr/local/ && \
    git clone https://github.com/tseemann/barrnap.git && \
    cd barrnap/bin && \
    chmod +x barrnap && \
    ln -s $PWD/barrnap /bin/ && \
    barrnap --help >/dev/null

# Make sure bedtools is installed
RUN bedtools --help > /dev/null
