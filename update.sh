# !/bin/bash
# ONLY RUN ON SERVER
# make sure to do "chmod +x <fileName>" first
git reset --hard HEAD
git pull
sudo systemctl restart cloudcopy
