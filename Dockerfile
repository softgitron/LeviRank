FROM python:3.9-alpine

# Create app directory
WORKDIR /app

# Install other required system level applications
RUN apk --no-cache add openjdk11 musl-dev linux-headers g++ pcre-dev \
gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev && \
pip install pipenv

# Install required python packages
COPY ./Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile --verbose

# Set necessary java environment variables
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk
ENV JDK_HOME /usr/lib/jvm/java-11-openjdk
ENV LD_LIBRARY_PATH /usr/lib/jvm/java-11-openjdk/lib/server/:/usr/lib/:/lib/

# Install special environments
RUN cd ./src/special_environments/t5_reranker && pipenv install -v

# Prepare libraries
COPY ./src/prepare_libraries.py ./src/prepare_libraries.py
COPY ./src/special_environments/t5_reranker/prepare_libraries.py ./src/special_environments/t5_reranke/prepare_libraries.py
RUN python ./src/prepare_libraries.py
RUN cd ./src/special_environments/t5_reranker && pipenv run python ./prepare_libraries.py

# Copy sources and premade index
COPY ./src/ ./
COPY ./data/index ./data/index

CMD ["python", "./src/main.py"]