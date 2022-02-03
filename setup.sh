# remove default python and its environment settings

# sudo apt purge -y python2.7
# sudo apt purge -y python3

# perform cleanup

sudo apt autoremove -y
apt-get update -y

# sudo apt-get install python3 -y
# sudo apt-get install python3-pip -y
alias python='/usr/bin/python3'
alias pip='/usr/bin/pip3'


# install dependencies for opencv

sudo apt-get install libcblas-dev -y
sudo apt-get install libhdf5-dev -y
sudo apt-get install libhdf5-serial-dev -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install libjasper-dev -y 
sudo apt-get install libqtgui4 -y
sudo apt-get install libqt4-test -y
cd Mobile\ Unit/
pip install -r requirements.txt
pip install numpy 
PATH=/home/pi/.local/bin:$PATH