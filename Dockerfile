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

# Prepare libraries
COPY ./src/prepare_libraries.py ./src/prepare_libraries.py
RUN python ./src/prepare_libraries.py

# Copy sources and data
COPY ./src/ ./
COPY ./data/corpus/touche-task2-passages-version-002.jsonl ./data/corpus
COPY ./data/titles/topics-task2.xml ./data/titles
RUN mkdir ./data/index

CMD ["python", "./src/main.py"]