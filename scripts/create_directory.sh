#!/bin/bash

# Ensure the AWS python API is installed
pip install awscli

pushd ~ubuntu

rm -rf geonetwork

mkdir geonetwork

popd
