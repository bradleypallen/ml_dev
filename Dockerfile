################################################################################
# Dockerfile to build an image for training and evaluating classification 
# and prediction models using Vowpal Wabbit and perf
# Based on Ubuntu
################################################################################

# Set the base image to Ubuntu
FROM ubuntu:latest

# File Author / Maintainer
MAINTAINER Bradley P. Allen "bradley.p.allen@gmail.com"

# Update the repository sources list
RUN apt-get update

# Install basic tools and required libraries
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q emacs
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q g++
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q wget
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python
RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q install build-essential python-dev python-pip python-setuptools
RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q install libboost-program-options-dev libboost-python-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q install zlib1g-dev
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv
RUN pip install --upgrade fabric

# Install ml_dev
RUN cd /home;git clone https://github.com/bradleypallen/ml_dev.git

# Install vw (Vowpal Wabbit) and perf
# Done using CMD to avoid problems with local machine architectural differences
CMD cd /usr/local/src;git clone https://github.com/bradleypallen/vowpal_wabbit.git;cd /usr/local/src/vowpal_wabbit;make;make test;make install;cd /usr/local/src;wget http://osmot.cs.cornell.edu/kddcup/perf/perf.src.tar.gz;tar xvf perf.src.tar.gz;rm perf.src.tar.gz;mv perf.src perf;cd /usr/local/src/perf;make -B perf;make install
