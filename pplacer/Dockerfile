FROM ubuntu:trusty

# Install dependencies
RUN apt-get -y update && \
    apt-get -y install camlp4-extra gawk libgsl0-dev libsqlite3-dev \
    libz-dev m4 wget make ocaml patch build-essential \
    git pkg-config unzip python-pip python-dev sqlite3

# Make needed folders
RUN mkdir /fh && \
    mkdir /app && \
    mkdir /pplacer && \
    mkdir /pplacer/src && \
    mkdir /data

# Install pplacer
RUN cd /pplacer/src && \
    wget https://raw.github.com/ocaml/opam/master/shell/opam_installer.sh -O - | sh -s /usr/local/bin && \
    ln -s /usr/local/bin/opam /usr/bin/opam && /usr/local/bin/opam init -y && \
    opam repo add pplacer-deps http://matsen.github.com/pplacer-opam-repository && \
    opam update pplacer-deps && eval `opam config env` && \
    git clone https://github.com/matsen/pplacer && \
    cd pplacer && \
    git checkout 1189285ce98de64cfa8c4f121c3afc5d8d03893f && \
    opam update && \
    opam install -y depext && \
    opam depext -y csv ounit xmlm mcl batteries ocaml-gsl sqlite3 camlzip && \
    opam install -y csv ounit xmlm mcl batteries ocaml-gsl sqlite3 camlzip && \
    eval $(opam config env) && \
    make && \
    cp /pplacer/src/pplacer/bin/* /usr/local/bin
    
# Install python dependencies
RUN pip install pip --upgrade && \
    pip install numpy biopython pandas --upgrade && \
    pip install bucket_command_wrapper==0.3.0 csvkit==1.0.2 \
                taxtastic==0.8.3

# Install pplacer scripts
RUN cd /pplacer/src/pplacer/scripts && \
    python setup.py install

WORKDIR /pplacer
