FROM nvidia/cuda:11.6.0-runtime-ubuntu20.04

# Create app directory
WORKDIR /app

# Install other required system level applications
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install openjdk-17-jdk g++ libpcre3-dev \
gcc gfortran build-essential wget curl libfreetype-dev libpng-dev libopenblas-dev libgomp1 git \
python3.9 python3.9-distutils python3.9-dev && ln /bin/python3.9 /bin/python && \
wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && pip install pipenv

# Install required python packages
COPY ./Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile --verbose

# Install special environments
COPY ./src/special_environments/t5_reranker/Pipfile* /app/src/special_environments/t5_reranker/
RUN cd ./src/special_environments/t5_reranker && pipenv install -v

# Prepare libraries
COPY ./src/prepare_libraries.py /app/src/prepare_libraries.py
RUN python /app/src/prepare_libraries.py
WORKDIR /app/src/special_environments/t5_reranker
COPY ./src/special_environments/t5_reranker/prepare_libraries.py /app/src/special_environments/t5_reranker/prepare_libraries.py
RUN pipenv run python ./prepare_libraries.py
WORKDIR /app

# Copy premade files and source codes
COPY ./data/ /app/data/
COPY ./src/ /app/src/

# Make directories for input and output files
RUN mkdir /app/data/in && mkdir /app/data/out

ENTRYPOINT ["python", "/app/src/main.py"]
CMD ["python", "/app/src/main.py"]