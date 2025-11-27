# Petoi Bittle — Steps for Windows and COM Port Connection

1. Hardware checklist
    - Petoi Bittle, USB cable (use data-capable cable), battery (charged), PC with Windows.

2. Install USB-to-serial driver
    - Bittle may use CH340/CP210x/FTDI/STM drivers. If Windows does not auto-install, download the matching driver from the chip vendor (CH340/CP210x/FTDI/STM) and install.

3. Get Petoi firmware and tools
https://docs.petoi.com/desktop-app/tools

4. Connect Bittle to PC
    - Connect the usb module to Bittle's NyBoard(main board).
    - Plug the battery into the Bittle.
    - Plug the USB cable from PC to Bittle’s USB port.

Optionals:
7. Configure Arduino IDE (or PlatformIO)
    - In Arduino IDE: Tools → Board → select the board indicated by Petoi docs (or the matching MCU).
    - Tools → Port → select the COMn from Device Manager.
    - Tools → Processor/Upload Speed: follow Petoi repo instructions (115200 or as documented).

8. Open and set up the firmware
    - Open the example/main sketch from the downloaded Petoi repo.
    - Edit any configuration constants if required (model, servo counts, initial calibration) following repo README.

9. Upload firmware
    - Press Upload in the IDE. If the board requires a manual reset/boot mode, follow the repository’s step (press reset button just before or during upload).
    - Wait until the IDE reports “Done uploading.” Resolve compile errors by installing missing libraries indicated by the IDE.


Quick troubleshooting tips
- If upload fails: try a different USB cable or port, reinstall driver, or reboot PC.
- If no COM port shows: check Device Manager for unknown devices and re-install appropriate driver.
- If servos don’t move after upload: ensure external battery is connected and powered (USB may not supply servo current).

References
- Follow the repository README for board-specific settings, libraries, and calibration steps.
