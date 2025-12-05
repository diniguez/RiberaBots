## Using WSL and windows drivers

# in windows web navigator, install driver for usb:
https://github.com/dorssel/usbipd-win/releases/download/v5.3.0/usbipd-win_5.3.0_x64.msi

# open a windows terminal
(Win+R)
cmd

# install and run wsl with ubuntu
wsl --install

wsl --install ubuntu

# create our user and remmember password (it doesn't appear the keys you press)

# open a Powershell terminal
wsl --version
# verify version is >= 2.0

usbipd list
# choose the busid of one USB where we will connect Petoi
usbipd bind --busid 1-4
usbipd attach --wsl --busid 1-4
exit

# go back to WSL terminal, create a folder for our project
cd
mkdir petoi
cd petoi

# open a Windows Explorer and find your local folder of Petoi
\\wsl$\Ubuntu\home\<<your user>>\petoi
# copy there the python files of the project (using mouse or/and copy&paste commands)

# in WSL terminal, install Python and libraries
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y pciutils build-essential libsndfile1-dev 
sudo apt install -y python3.10 python3.10-venv python3.10-distutils python3.10-dev
sudo apt install curl
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo /usr/bin/python3.10

# create and work into the virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# add libraries
pip install pyserial

# give access to the Petoi connection port usb, exactly to the /dev/ttyACM0
sudo usermod -a -G dialout vespertino
sudo chmod +777 /dev/ttyACM0

# run the code
python3.10 manual_control_pc.py


# #OPTIONALS# #####################################################################################
# in WSL terminal, install vosk spanish model
mkdir -p my_vosk/models
cd my_vosk/models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
sudo apt install -y unzip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip

# install Python headers, PortAudio dev headers and build tools
sudo apt install -y portaudio19-dev libportaudio2
pip install vosk sounddevice soundfile
exit

# restart user session (close and open WSL terminal)
cd $folderOfPetoi
source .venv/bin/activate

# run the code
python3.10 voice_control_pc.py
