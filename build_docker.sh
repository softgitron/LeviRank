#!/bin/bash
docker build ./ -t touche-2022
if [ $? -eq 0 ]; then
    docker save touche-2022:latest | pigz > touche-2022-docker-image.tar.gz
    docker tag touche-2022 localhost:5000/touche-2022
    # docker push localhost:5000/touche-2022
fi