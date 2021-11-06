FROM ubuntu:18.04

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

ENV DEBIAN_FRONTEND noninteractive
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
            python3                        \
            python3-pip                    \  
            python3-opencv              && \
            apt-get autoremove          && \          
            apt-get clean               && \                
            rm -rf /var/lib/apt/lists/* && \
            pip3 install --no-cache-dir    \
            pip                            \
            setuptools                  && \
            python3 -m pip install --upgrade pip
ENV DEBIAN_FRONTEND noninteractive

RUN pip3 --no-cache-dir install --upgrade \    
    opencv-python