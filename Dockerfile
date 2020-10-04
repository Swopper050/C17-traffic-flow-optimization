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

# install cityflow
RUN apt -y install libspatialindex-c4v5 python3-pip
RUN pip install --upgrade pip
RUN pip install flask
RUN cd /home/
RUN git clone https://github.com/cityflow-project/CityFlow.git
RUN cd CityFlow && \
    pip install .
RUN pip install -Iv matplotlib==3.3.1
RUN pip install -Iv mesa==0.8.7
RUN pip install rtree
RUN pip install -Iv osmnx==0.15.1
RUN pip install -Iv seaborn==0.11.0
RUN pip install -Iv black==20.8b1
RUN pip install -Iv flake8==3.8.3
RUN pip install -Iv isort==5.5.0
COPY . /home/C17-traffic-flow-optimization
RUN cd /home/C17-traffic-flow-optimization/ && \
    python3 run_static_routing_simulation.py
