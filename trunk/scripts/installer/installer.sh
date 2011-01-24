#!/bin/bash

#	DO NOT DISTRIBUTE - contains database login info for edsa.aurorardc.aero

MYPATH=`dirname $0`

#	Check that we are root
if [[ $EUID -ne 0 ]]; then
   echo "Please run the EDSA installer as root or within 'sudo.'" 1>&2
   exit 1
fi

DEFAULT_INSTALL_DIR=/usr/share/edsa

#	Copy source code to install directory
echo "Welcome to the EDSA installer!"
echo "------------------------------"
echo "If at any point you feel something has gone wrong, press Ctrl-C to exit."
echo
echo "Software and libraries required for EDSA will be installed in their"
echo "default locations."
echo
echo "Please enter the directory in which you would like to place the"
echo "EDSA source code.  (Hit enter without typing anything to accept"
echo "the default of $DEFAULT_INSTALL_DIR)."
echo -n " -> "
read -e INSTALL_DIR
if [[ ! $INSTALL_DIR ]]
then
	INSTALL_DIR=$DEFAULT_INSTALL_DIR
fi
echo "Selected: $INSTALL_DIR"
cp -r ./src $INSTALL_DIR

while [[ ! $MACHINE_NAME ]]
do
	echo -n "Please enter a name for this machine (no spaces please) -> "
	read MACHINE_NAME
done
echo "Selected: $MACHINE_NAME"

IP_ADDRESS=`ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
echo "Please enter the IP address of this machine"
echo -n "(hit enter for default: $IP_ADDRESS) -> "
read IP_ADDRESS_NEW
if [[ $IP_ADDRESS_NEW ]]
then
	IP_ADDRESS=$IP_ADDRESS_NEW
fi
echo "Selected: $IP_ADDRESS"

#	Software Dependencies
echo
echo "EDSA will now attempt to install software that is needed for all of its"
echo "features to work.  This may take several minutes, especially if you have"
echo "a slow Internet connection."
echo
echo "Installing software dependencies..."
apt-get install -y python python-dev python-gtk2-dev python-setuptools subversion openvpn libpq-dev libfreetype6-dev libpng12-dev python-dateutil xfoil > install.log

#	Python Library Dependencies
echo "Installing Python libraries..."
python -m easy_install django >> install.log
python -m easy_install psycopg2 >> install.log
python -m easy_install Pyro==3.10 >> install.log
python -m easy_install feincms >> install.log
python -m easy_install django-extensions >> install.log
python -m easy_install django-mptt >> install.log
python -m easy_install South >> install.log
python -m easy_install simplejson >> install.log

#	Forcing numpy download to work
if [[ ! -e numpy-1.5.0.tar.gz ]]
then
	wget -O numpy-1.5.0.tar.gz http://downloads.sourceforge.net/project/numpy/NumPy/1.5.0/numpy-1.5.0.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fnumpy%2Ffiles%2FNumPy%2F >> install.log
fi
python -m easy_install numpy-1.5.0.tar.gz &>> install.log

#	Forcing matplotlib to come from version that isn't buggy with GCC 4.4
#	python -m easy_install matplotlib >> install.log
if [[ ! -e matplotlib-1.0.0.tar.gz ]]
then
	wget -O matplotlib-1.0.0.tar.gz http://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.0/matplotlib-1.0.0.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fmatplotlib%2Ffiles%2F >> install.log
fi
python -m easy_install matplotlib-1.0.0.tar.gz &>> install.log

#	Todo: install Qprop

#	EDSA settings
FEINCMS_LOC=`$MYPATH/get_feincms_path.py`
echo "Configuring EDSA local_settings.py..."
echo "EDSA_IP_ADDRESS = '$IP_ADDRESS'
EDSA_MACHINE_NAME = '$MACHINE_NAME'
EDSA_ROOT = '$INSTALL_DIR/'
EDSA_TOOL_WORKDIR = EDSA_ROOT + 'tools/'
EDSA_STORAGE_DIR = EDSA_ROOT + 'files/'
EDSA_TOOL_PATH = (
    EDSA_ROOT + '/tools',
    EDSA_ROOT + '/tools/xfoil',
)
PROJECT_ROOT = EDSA_ROOT
FEINCMS_ADMIN_MEDIA_LOCATION = '$FEINCMS_LOC'

DEBUG_TOOLBAR_CONFIG = {}
DEBUG_TOOLBAR_CONFIG['INTERCEPT_REDIRECTS'] = False
INTERNAL_IPS = ['127.0.0.1', '$IP_ADDRESS']
" > $INSTALL_DIR/edsa/local_settings.py
#	Database login info specific to edsa.aurorardc.aero
echo "DATABASE_USER = 'edsa'
DATABASE_PASSWORD = 'geVepHa3'
" > $INSTALL_DIR/edsa/database_settings.py

#	Execute permissions should be there already but...
chown -R `echo $HOME | cut -f 3- -d/` $INSTALL_DIR
chmod +x $INSTALL_DIR/edsa/daemon.py
chmod +x $INSTALL_DIR/edsa/manage.py
chmod +x $INSTALL_DIR/start.sh
chmod +x $INSTALL_DIR/stop.sh

#	Start/stop scripts
ln -s $INSTALL_DIR/start.sh "$HOME/Desktop/Start EDSA Client"
ln -s $INSTALL_DIR/stop.sh "$HOME/Desktop/Stop EDSA Client"

#	Directions
echo
echo "Installation is complete."
echo
echo "To use EDSA, you can cd to $INSTALL_DIR/edsa and run in separate terminals:"
echo "    ./daemon.py		(to host tools and files)"
echo "    ./manage.py runserver [address][:[port]] (to run Web interface)"
echo "Or, if you are using a graphical environment, try the shortcuts on your Desktop."



