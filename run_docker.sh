#!/bin/bash

# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
while [[ $# -gt 0 ]]; do
  case $1 in
    -i)
      INPUT_PATH=$(realpath $2)
      shift # past argument
      shift # past value
      ;;
    -o)
      OUTPUT_PATH=$(realpath $2)
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      shift # past argument
      ;;
  esac
done

if [ -z "$INPUT_PATH" ]; then
  echo "Input not set"
  exit 2
fi
if [ -z "$OUTPUT_PATH" ]; then
  echo "Ouput not set"
  exit 3
fi


docker run --gpus '"device=0"' --mount type=bind,source="$INPUT_PATH",target=/app/data/in --mount type=bind,source="$OUTPUT_PATH",target=/app/data/out touche-2022 -i /app/data/in -o /app/data/out