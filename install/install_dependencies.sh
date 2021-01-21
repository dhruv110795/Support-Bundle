#!/bin/sh

sudo apt-get update
BASE_APT_CMD="sudo apt install -y "
BASE_PIP_CMD="sudo python3 -m pip install "
PYTHON_DEPENDENCIES="python3-pip python3-dev zlib1g"
PYTHON_MODULES="bottle pyminizip psutil humanize twisted"

#python-pip modules installer function
install_python_module()
{
    echo "#############################################################################################\n\n"
    echo "Installing python module--> $1 "
    CMD=$BASE_PIP_CMD$1
    if $CMD;then echo ""
    else
	echo "\nUnable to install $1 module\n"
	exit 1
    fi
    echo "#############################################################################################\n\n"
}


#APT-Package installer function
install_package()
{
    echo "################################################################################################\n\n"
    echo "Installing package--> $1"
    CMD=$BASE_APT_CMD$1
    if $CMD;then echo ""
    else
        echo "Trying with Manual installation without -y"
        if sudo apt install $1; then echo ""
        else
            echo "\nUnable to install $1 package\n"
            exit 1
        fi

    fi
    echo "################################################################################################\n\n"
}

for dep in $PYTHON_DEPENDENCIES
do
    install_package $dep
done

for dep in $PYTHON_MODULES
do
    install_python_module $dep
done

if [ ! -e /lib/systemd/system/SupportBundle.service ]
then
    sudo cp SupportBundle.service /lib/systemd/system/SupportBundle.service
    sudo systemctl daemon-reload
    sudo systemctl enable SupportBundle.service
fi
sudo systemctl start SupportBundle.service

(crontab -l 2>/dev/null; echo "0 0 * * * /usr/bin/python3 $PWD/clear_tmp_files.py") | crontab -

echo "Use http://IP:9090 to view karthavya support bundle web"
