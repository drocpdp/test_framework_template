# linux update
### rh
#sudo yum update 
### suse - requires "y" prompt
sudo zypper -n update

# create directories
sudo mkdir /opt/testing
sudo mkdir /opt/testing/configs
sudo mkdir /opt/testing/configs/run_configs
sudo mkdir /opt/testing/configs/run_configs/test_runs
sudo mkdir /opt/testing/virtualenvs
sudo mkdir /opt/testing/virtualenvs/$PROJECT_NAME
sudo mkdir /opt/testing/reports
sudo mkdir /opt/testing/reports/old_reports
sudo mkdir /opt/testing/$PROJECT_NAME

# set permissions
sudo chmod -R 777 /opt/testing/

# install python3
### rh
#sudo yum install python36
### suse
sudo zypper -n install python3

# install and upgrade pip3
### rh
#sudo yum install python-pip
#sudo pip3 install --upgrade pip
### suse (pip3 already installed)
sudo pip3 install --upgrade pip

# install/upgrade virtualenv
pip3 install virtualenv --upgrade

# create and update python virtualenv
python3 -m virtualenv /opt/testing/virtualenvs/$PROJECT_NAME

# activate virtualenv
source /opt/testing/virtualenvs/$PROJECT_NAME/bin/activate

# install git
### rh
#sudo yum install git
### suse - requires "y" prompt
sudo zypper -n install git

# clone git repo - requires password
git clone https://drocpdp@bitbucket.org/drocpdp/$PROJECT_NAME.git /opt/testing/$PROJECT_NAME

# install project pip requirements
pip3 install -r /opt/testing/$PROJECT_NAME/requirements.txt
