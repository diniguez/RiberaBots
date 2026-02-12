# Install VMWare on Linux:
# get the file VMware-Workstation-Full-17.6.4-24832109.x86_64.bundle
# give execution permission
chmod +777 VMware-Workstation-Full-17.6.4-24832109.x86_64.bundle 
# run the installer
sudo ./VMware-Workstation-Full-17.6.4-24832109.x86_64.bundle 

# After completing the hardware building, connect to the power supply.

# Connect HDMI cable, then usb keyboard and mouse.

# Turn on jetracer power.

# jetson/jetson user password for log in.

Connect to same wifi as laptop pc.

Obtain ip address from jetson lcd screen, annotate it (10.249.73.33)

Use that ip address to connect through wifi using ssh:
ssh jetson@10.249.73.33

# NOW YOU ARE IN THE ROBOT SYSTEM

hostname to obtain of the virtual machine
nano-4gb-jp451

# OPEN OTHER TERMINAL IN YOUR COMPUTER
# become sudoer
su ribera

# install nano editor
sudo apt install nano

# edit bash default configuration
sudo nano ~/.bashrc

# check the end lines to be:
export ROS_MASTER_URI=http://nano-4gb-jp451:11311 #Set the robot as the host
export ROS_HOSTNAME=nano-4gb-jp451

# otherwise, add them, save the file and execute:
source ~/.bashrc

# IN YOUR VIRTUAL MACHINE
ifconfig       #Get the IP address of the virtual machine
hostname       #Get the hostname of the virtual machine

sudo nano ~/.bashrc

Add at the end:
export ROS_MASTER_URI=http://nano-4gb-jp451:11311     #Point to the robot host
export ROS_HOSTNAME=ubuntu    #or the one you have configured

After the addition is complete, run the following command to take effect:
source ~/.bashrc

# IN THE ROBOT SYSTEM
sudo nano /etc/hosts

edit the line that says 192.168.xxx.xxx to be the one of your laptop pc (obtained with ifconfig and hostname commands)
for example, mine is:
10.74.153.99    ubuntu

# IN YOUR VIRTUAL MACHINE
sudo nano /etc/hosts

edit the line that says 192.168.xxx.xxx or add a new line to be the one of the robot (obtained with ifconfig and hostname commands)
for example, my robot is:
10.74.153.94     nano-4gb-jp451

# Add the user to the communication buffer file
sudo adduser jetson dialout

# if the answer is different to: "The user `jetson' is already a member of `dialout'.
sudo reboot
# and connect again with ssh

## TEST CONNECTION
# launch in the robot
rosrun rospy_tutorials listener 
# launch in the virtual machine
rosrun rospy_tutorials talker

---
# Optional step:
https://www.waveshare.com/wiki/JetRacer_ROS_AI_Kit_Advanced_Tutorial_VI:_Install_ROS_System_in_Ubuntu_Virtual_Machine_%26_Environment_Configuration#:~:text=by%20VMware%20software.-,Step%201%3A%20Configure%20ROS%20Software%20Repository,-After%20installing%20the

 is to find the right ROS software repository from http://packages.ros.org/ros/ubuntu/dists/?C=M;O=A as they have been discontinued by organization https://wiki.ros.org/noetic/Planning/Maintenance:
The last ROS 1 release Noetic will go end of life on May 31st with that the ROS Wiki (this website) will also be EOL and transition to being an archive. Maintainers:Please migrate any wiki content into your package's README.md file. If you need more help on migrating code please see this migration guide. Or watch Shane's Lightning Talk from ROSCon 2024(https://vimeo.com/1026038503?share=copy#t=392.022).


## Optional environent set up for IES Ribera ubuntu laptops:
su ribera
usermod -aG sudo vespertino
groups vespertino
visudo 
# if visudo is not available, run: sudo apt install sudo
nano /etc/sudoers


## CONTROL ROBOT BY THE KEYBOARD:
# In the robot system (through SSH)
roscore
# open a new SSH connection
# drive the car by keyboard
roslaunch jetracer jetracer.launch

# In the VM console (not SSH):
rostopic list
