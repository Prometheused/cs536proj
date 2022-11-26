# install Mininet
git clone https://github.com/mininet/mininet
mininet/util/install.sh -a

# install Python, numpy, matplotlib, argparse
sudo apt-get install build-essential check install 
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
cd /usr
sudo chmod -r 777 src
cd /usr/src
sudo apt-get install python-pip
export LC_ALL=C
sudo pip install numpy
sudo pip install matplotlib
sudo pip install argparse
