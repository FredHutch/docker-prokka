# Docker Sciluigi Tools

Set of Docker images containing tools made by others, including a simple wrapper to enable sciluigi to wrap around these tools.

Current tools:

  * Prokka: [![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/prokka/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/prokka) Based on ummidock/prokka from [https://github.com/B-UMMI/docker-images](https://github.com/B-UMMI/docker-images).

  * Pplacer [![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/pplacer/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/pplacer) Compiled from [github.com/matsen/pplacer](github.com/matsen/pplacer) based on Ubuntu 14.04.

  * CheckM [![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/checkm/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/checkm) Based on the pplacer image in this repo.

  * Finch-rs [![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/finch-rs/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/finch-rs) See [https://github.com/onecodex/finch-rs](https://github.com/onecodex/finch-rs) for details.

  * fastqp [![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/fastqp/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/fastqp) See [https://github.com/mdshw5/fastqp](https://github.com/mdshw5/fastqp) for details.

  * python [![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/python/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/python)


### Triggering builds on Quay

My practice is to configure the build triggers so that they only are started by tags that start with the tool name. This is to decrease the number of unneeded builds and keep everything more easily trackable. Therefore, if you change a tool you need to make a release (or tag) on GH that starts with the tool name in order for those changes to get propogated to Quay.
