FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app/

# Install necessary system dependencies
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
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
            /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
            rm /tmp/miniconda.sh

# Set up conda into the environment
ENV PATH /opt/conda/bin:$PATH

# Create a new Conda environment named "langchain" with Python 3.10
RUN /opt/conda/bin/conda create -n langchain python=3.10 -y

# Activate the Conda environment and clone the repository
RUN /bin/bash -c "source /opt/conda/bin/activate langchain && \
    git clone https://github.com/intel/intel-extension-for-transformers.git && \
    cd intel-extension-for-transformers && \
    pip install -r requirements.txt && \
    python3 setup.py install"

# Set the entrypoint to a bash shell
ENTRYPOINT ["/bin/bash"]


# Change directory to the app directory
WORKDIR /app/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["exec", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]