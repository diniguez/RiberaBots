After completing the hardware building, connect to the power supply.

Connect HDMI cable, then usb keyboard and mouse.

Turn on jetracer power.

jetson/jetson user password for log in.

Connect to same wifi as laptop pc.

Obtain ip address from jetson lcd screen, annotate it (10.74.153.182)

Use that ip address to connect through wifi using ssh:
ssh jetson@10.74.153.182
NOW YOU ARE ON THE ROBOT SYSTEM

hostname to obtain of the virtual machine
nano-4gb-jp451

sudo apt install nano  #install nano editor

sudo nano ~/.bashrc

check the end lines to be:
export ROS_MASTER_URI=http://nano-4gb-jp451:11311 #Set the robot as the host
export ROS_HOSTNAME=nano-4gb-jp451

otherwise, add them, save the file and execute:
source ~/.bashrc

In your laptop or PC, ubuntu S.O. do:
ifconfig       #Get the IP address of the virtual machine
hostname       #Get the hostname of the virtual machine

sudo nano ~/.bashrc

Add at the end:
export ROS_MASTER_URI=http://nano-4gb-jp451:11311     #Point to the robot host
export ROS_HOSTNAME=ubuntu    #or the one you have configured

After the addition is complete, run the following command to take effect:
source ~/.bashrc

Robot system:
sudo nano /etc/hosts

edit the line that says 192.168.xxx.xxx to be the one of your laptop pc (obtained with ifconfig and hostname commands)
for example, mine is:
10.74.153.99    david-aorus

Laptop system:
sudo nano /etc/hosts

edit the line that says 192.168.xxx.xxx to be the one of your laptop pc (obtained with ifconfig and hostname commands)
for example, mine is:
10.74.153.99    david-aorus

Install VMWare Workstation PRO
Run VM Ubuntu Jetracer 18.04


---
Optional step:
https://www.waveshare.com/wiki/JetRacer_ROS_AI_Kit_Advanced_Tutorial_VI:_Install_ROS_System_in_Ubuntu_Virtual_Machine_%26_Environment_Configuration#:~:text=by%20VMware%20software.-,Step%201%3A%20Configure%20ROS%20Software%20Repository,-After%20installing%20the

 is to find the right ROS software repository from http://packages.ros.org/ros/ubuntu/dists/?C=M;O=A as they have been discontinued by organization https://wiki.ros.org/noetic/Planning/Maintenance:
The last ROS 1 release Noetic will go end of life on May 31st with that the ROS Wiki (this website) will also be EOL and transition to being an archive. Maintainers:Please migrate any wiki content into your package's README.md file. If you need more help on migrating code please see this migration guide. Or watch Shane's Lightning Talk from ROSCon 2024(https://vimeo.com/1026038503?share=copy#t=392.022).