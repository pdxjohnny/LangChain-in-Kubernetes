# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim

COPY . .
# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    git \
    build-essential \
    autoconf \
    && rm -rf /var/lib/apt/lists/*

# Download and install Miniconda
ENV MINICONDA_VERSION="latest"
ENV MINICONDA_INSTALLER="Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh"
RUN wget -q "https://repo.anaconda.com/miniconda/${MINICONDA_INSTALLER}" -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

# Set up conda into the environment
ENV PATH="/opt/conda/bin:$PATH"

# Create a new Conda environment named "langchain" with Python 3.10
RUN conda create -n langchain python=3.10 -y && \
    conda init bash

# Activate the Conda environment and install dependencies
# Activate the Conda environment and install dependencies
SHELL ["conda", "run", "-n", "langchain", "/bin/bash", "-c"]

RUN conda install -y -c conda-forge gxx gcc gdb sysroot_linux-64 && \
    git clone https://github.com/intel/intel-extension-for-transformers.git && \
    cd intel-extension-for-transformers && \
    git checkout 3e7e3530dcc0b6fb714cbb632fcb0d66ca2604c9 && \
    pip3 install -r requirements.txt && \
    python setup.py install

# Set environment variables
ENV LD_PRELOAD="/opt/conda/envs/langchain/lib/libstdc++.so.6"

# Install additional requirements from the requirements.txt file within the Conda environment
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Set the entrypoint to run the application
CMD ["/opt/conda/bin/conda", "run", "-n", "langchain", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]