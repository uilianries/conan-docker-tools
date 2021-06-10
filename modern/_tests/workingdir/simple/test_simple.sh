#!/bin/bash

set -ex

mkdir -p /tmp/build/simple
rm -rf /tmp/build/simple/*

pushd /tmp/build/simple

cmake /tmp/workingdir/simple -DCMAKE_BUILD_TYPE=Release
cmake --build .

./example-c
./example-cpp
