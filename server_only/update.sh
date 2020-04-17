# !/bin/bash
# ONLY RUN ON SERVER
# make sure to do "chmod +x <fileName>" first
cd cloud-copy
git pull
source cloudcopyenv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart cloudcopy
