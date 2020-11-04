FROM ubuntu:16.04

# c++ dependencies
RUN apt update && \
    apt-get install -y build-essential cmake wget git

# install Miniconda Python 3.6
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN wget -P /tmp/ https://repo.continuum.io/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh && \
    /bin/bash /tmp/Miniconda3-4.5.4-Linux-x86_64.sh -b -p /opt/conda && \
    rm /tmp/Miniconda3-4.5.4-Linux-x86_64.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

# install packages
RUN apt -y install libspatialindex-c4v5 python3-pip
RUN pip install --upgrade pip==10.0.1
RUN cd /home/
RUN git clone https://github.com/cityflow-project/CityFlow.git
RUN cd CityFlow && \
    pip install .
COPY . /home/C17-traffic-flow-optimization
RUN cd /home/C17-traffic-flow-optimization && \
    pip install -r requirements.txt
