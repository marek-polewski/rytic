#!/bin/bash

set -e

AMI="ami-030dbca661d402413" # amazon linux 2

# this is minimal set of arguments
#aws ec2 run-instances --user-data file://init.sh --image-id "$AMI"


# but we preffer those also defined
SG="sg-03cf4ed9434e7af90" # with tcp:80 open
TYPE="t3.nano" # instead of default m1.micro
SSHKEY="userx" # so we can connect to intance

aws ec2 run-instances --user-data file://jupyther.sh \
        --image-id "$AMI" \
        --instance-type "$TYPE"  \
	--key-name "$SSHKEY" \
        --security-group-ids "$SG" \
        --tag-specifications "{\"ResourceType\":\"instance\",\"Tags\":[{\"Key\":\"Name\",\"Value\":\"junypt\"}]}" # and name tag

