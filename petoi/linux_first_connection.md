# open a terminal / console
mkdir petoi 
cd petoi

su ribera

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-distutils
sudo apt install curl
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo /usr/bin/python3.10

# install vosk spanish model
mkdir -p my_vosk/models
cd my_vosk/models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip

# create and work into the virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# install Python headers, PortAudio dev headers and build tools
sudo apt install -y python3.10-dev portaudio19-dev libportaudio2 build-essential libsndfile1-dev 

pip install vosk sounddevice soundfile pyserial

# change vespertino for the right user name
sudo usermod -a -G dialout vespertino
sudo chmod +777 ttyACM0 
# this two last commands gives access to the Petoi connection port usb, exactly to the /dev/ttyACM0

# restart user session
cd $folderOfPetoi
source .venv/bin/activate

# run the code
python3.10 voice_control_pc.py
python3.10 manual_control_pc.py