#!/bin/bash
docker build ./ -t touche-2022
if [ $? -eq 0 ]; then
    docker save touche-2022:latest | pigz > touche-2022-docker-image.tar.gz
fi