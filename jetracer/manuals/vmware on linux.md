## Fix vmware opening image (make kernel certified driver)
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=Diniguez/"
sudo /usr/src/kernels/6.14.0-35-generic/scripts/sign-file sha256 ./MOK.priv ./MOK.der $(modinfo -n vmmon)
sudo mokutil --import MOK.der
# Now you just need to reboot and follow the screen menus that will appear during the UEFI boot to enroll the new key (on ubuntu 16 it's automatic it seems).

## Fix bridge connection
