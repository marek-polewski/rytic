#!/bin/bash

DIR="/srv/gallery"
mkdir -p "$DIR"

yum install -y awscli

aws s3 sync s3://public.czycytryny.pl/ "$DIR"

cd "$DIR"
python -m SimpleHTTPServer 80
