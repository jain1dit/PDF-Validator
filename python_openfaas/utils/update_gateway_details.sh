#!/bin/bash

echo "enter gateway IP address:"
read ghost

echo "enter gateway port number:"
read gport

for yaml_file in $(ls ../yaml/*.yml)
do
    sed -i "s/GATEWAY_HOST:GATEWAY_PORT/${ghost}:${gport}/g" ${yaml_file}
    echo "${yaml_file} updated"
done
