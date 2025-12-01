# WSL
## from a terminal, run wsl
wsl --install

wsl --install ubuntu

# create our user and remmember password

# in windows app, install driver for usb:
https://github.com/dorssel/usbipd-win/releases/download/v5.3.0/usbipd-win_5.3.0_x64.msi

# in Powershell
wsl --version
# verify version is >= 2.0

usbipd list
# choose the busid of one USB where we will connect Petoi
usbipd bind --busid 1-4
usbipd attach --wsl --busid 1-4

# in wsl, create a folder for our project
cd
mkdir petoi
cd petoi

# open your local folder of Petoi from Windows Explorer
\\wsl$\Ubuntu\home\vespertino\petoi
# copy there the python files of the project (using mouse and copy&paste commands)


# install Python and libraries
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
# install vosk spanish model
mkdir -p my_vosk/models
cd my_vosk/models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip

# install Python headers, PortAudio dev headers and build tools
sudo apt install -y portaudio19-dev libportaudio2
pip install vosk sounddevice soundfile

# restart user session
cd $folderOfPetoi
source .venv/bin/activate

# run the code
python3.10 voice_control_pc.py
