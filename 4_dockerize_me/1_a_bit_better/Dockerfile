FROM amazonlinux:latest

ENV DIR /srv/gallery

RUN yum install -y awscli && \
	mkdir -p "$DIR"

#RUN aws s3 sync s3://public.czycytryny.pl/ "$DIR"

WORKDIR "$DIR"
CMD ["python", "-m", "SimpleHTTPServer", "80"]
