#!/bin/bash

yum update -y

DIR="/srv/gallery"
mkdir -p "$DIR"

aws s3 sync s3://public.czycytryny.pl/ "$DIR"

cd "$DIR"
python -m SimpleHTTPServer 80
