#!/bin/bash

set -e

yum update -y

curl https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh -o anaconda.sh
chmod +x anaconda.sh
./anaconda.sh -b -p /opt/anaconda

sudo -u ec2-user /opt/anaconda/bin/jupyter notebook --generate-config -y

echo "c.NotebookApp.allow_remote_access = True" >> /home/ec2-user/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.ip = '*'" >> /home/ec2-user/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> /home/ec2-user/.jupyter/jupyter_notebook_config.py

/opt/anaconda/bin/python3 -m pip install --upgrade pip
/opt/anaconda/bin/python3 -m pip install jupyter

sudo -u ec2-user screen -dm bash -c "cd /home/ec2-user && /opt/anaconda/bin/jupyter notebook"


