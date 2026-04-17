## para linux:
# la primera vez:
# su ribera
# sudo nano /etcsudoers
# vespertino ALL=(ALL:ALL) ALL
# exit
# sudo apt update
# sudo apt install python3-venv
# python3 -m venv venv
# source env/bin/activate
# pip install djitellopy
# pyhton3 dron.py

# en lo sucesivo:
# source env/bin/activate
# pyhton3 dron.py


## para Windows:
1. Install python with all main libraries
sudo apt install python3-full

2. Install pip:
sudo apt install python3-pip.

3. Install venv (if not already installed):
sudo apt install python3-venv.

4. Crete our own folder for the project
mkdir miCarpeta

5. Create the virtual environment:
python3 -m venv miCarpeta

6. Activate the environment:
source miCarpeta/bin/activate
