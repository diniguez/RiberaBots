# open a terminal / console
mkdir petoi 
cd petoi

# work as a superadmin for SW installation
su ribera

# install or check that curl is installed
sudo apt install -y curl

# install Python for developers
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo /usr/bin/python3.10

# create the virtual environment
sudo python3.10 -m venv .venv

# work into the virtual environment
source .venv/bin/activate

# install Python headers and build tools
sudo apt install -y python3.10-dev build-essential

# install serial ports communication
pip install pyserial


### CONNECT BY BLE (BLUETOOTH LOW ENERGY) ############
bluetoothctl
scan on
# if PetoiBLE appears, you can run test_ble.py
# otherwise, restart BT from Ubuntu and repeat
sudo systemctl restart bluetooth

# modify MAC ADDRESS into code variable ADDRESS


### CONNECT BY USB CABLE ### Serial connection
# this two last commands gives access to the Petoi connection port usb, exactly to the /dev/ttyACM0
sudo usermod -a -G dialout vespertino
sudo chmod +777 /dev/ttyACM0

# restart user session
cd $folderOfPetoi
source .venv/bin/activate

# work as the normal user
exit

# go to Petoi folder
cd
cd petoi

# run the code
python3.10 manual_control_pc.py

### CONNECT BY BLUETOOTH (no BLE) ############
bluetoothctl
disconnect 54:37:45:9A:9A:E1
connect 54:37:45:9A:9A:E1
quit

sudo rfcomm bind /dev/rfcomm0 54:37:45:9A:9A:E1
#sudo rfcomm bind /dev/rfcomm0 54:37:45:9A:9A:63

### extra tests for BT ##########
sdptool browse 54:37:45:9A:9A:E1

# # ###############################################################################################
## OPTIONAL
# # ###############################################################################################
# install vosk spanish model
cd
cd petoi
mkdir -p my_vosk/models
cd my_vosk/models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip

# install PortAudio dev headers
su ribera
sudo apt install -y portaudio19-dev libportaudio2 libsndfile1-dev
# install vosk and sound device
exit
pip install vosk sounddevice soundfile

# run the code
python3.10 voice_control_pc.py
