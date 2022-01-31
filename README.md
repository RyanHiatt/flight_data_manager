# Flight Data Retrieval and Management System

## Project Overview

### Table of Contents
- [Geekworm X735 V2.5 Shield Installation](https://github.com/RyanHiatt/flight_data_manager)
  - [Installation]
  - [Software]
- [Connecting the Official Raspberry Pi 7in Touchscreen]
- [Interfacing the SD Card Module](https://github.com/RyanHiatt/flight_data_manager#interfacing-the-sd-card-module)
  - [Wiring](https://github.com/RyanHiatt/flight_data_manager#wiring)
  - [Software Setup](https://github.com/RyanHiatt/flight_data_manager#software-setup)
- [Creating Raspberry Pi Backup Images]
  - [Linux]
  - [macOS]


## Geekworm X735 V2.5 Shield Installation

[![Geekworm X735 V2.5 Shield](/static/images-github/geekworm_x735_v2-5.png)](https://www.amazon.com/Geekworm-Raspberry-Management-Expansion-Compatible/dp/B07R45W1LN/ref=pd_bxgy_img_2/147-1032413-0120637?pd_rd_w=GVGAz&pf_rd_p=6b3eefea-7b16-43e9-bc45-2e332cbf99da&pf_rd_r=N3J44B70SEC8CYZ6RK8T&pd_rd_r=0e130e86-118a-493c-8063-24000bf0cc8f&pd_rd_wg=ShFxX&pd_rd_i=B07R45W1LN&psc=1)

### Installation



### Software

#### Install

1. To begin ensure the system is up-to-date:
```shell
sudo apt update && sudo apt upgrade
```

2. Next, the following can be run line by line to install the required packages, 
clone the repository(I cloned mine in the 'home' repository), and give permissions:
```shell
sudo apt-get install -y python-smbus python
sudo apt-get install -y pigpio python-pigpio python3-pigpio git
git clone https://github.com/geekworm-com/x735-v2.5
cd x735-v2.5
sudo chmod +x *.sh
sudo bash install.sh
echo "alias x735off='sudo x735softsd.sh'" >> ~/.bashrc
sudo reboot
```

3. To have the script run automatically when the device is restarted, it will have to be added to the bashrc profile:
```shell
nano ~/.bashrc 
```
and copy the following to the bottom of the file:
```shell
python /home/pi/x735-v2.5/pwm_fan_control.py & 
```
> Note: You may have to change the file path depending on your OS or where you initially cloned the repository.

4. Last step is to test it is working properly using the following:
   1. `x735off` is safe shutdown command, you can run this command to safe shutdown.
   2. Press onboard button 1-2 seconds to reboot
   3. Press onboard button 3 seconds to safe shutdown,
   4. Press onboard button 7-8 seconds to force shutdown.

6. Extra: this script allows for live readings of the pwm fan rpm, this can be done by running `python3 x735-v2.5/read_fan_speed.py`.
This however can be a bit tedious especially if you are starting from a different directory, therefore I like to add
an alias to the `~/.bashrc` profile to be able to input `fanspeed` into the terminal and get the results:
```shell
echo "alias fanspeed='python3 home/pi/python3 x735-v2.5/read_fan_speed.py'" >> ~/.bashrc
```

#### Uninstall

To uninstall the scripts, cd into the scripts directory `cd x735-v2.5` and run:
```shell
sudo unistall.sh
```


## Connecting the Official Raspberry Pi 7in Touchscreen


## Interfacing the SD Card Module

For this project flight data is accumulated to a full size sd card, however the raspberry pi doesn't have support for a
full size sd card. One option would be to use a USB dongle, but taking into consideration aesthetics and having the
ability to build a sd card reader into the device enclosure. I opted for a sd card module using SPI.

[![SD Card Module](/static/images-github/sd_card_module.png)](https://www.amazon.com/dp/B07XGQ863W?psc=1&ref=ppx_yo2_dt_b_product_details)

&nbsp;

### Wiring

| SD Card Module  |     Raspberry Pi 4B     |   
|:---------------:|:-----------------------:|
|       GND       |         Ground          |
|       3V3       |        3V3 power        |
|       5V        |      Not Connected      |
|       CS        |  Pin 24 - GPIO 8 (CE0)  |
|      MOSI       | Pin 19 - GPIO 10 (MOSI) |
|       SCK       | Pin 23 - GPIO 11 (SCLK) |
|      MISO       | Pin 21 - GPIO 9 (MISO)  |
|       GND       |      Not Connected      |


> Note: Use either 3V3 or 5V the module supports either one but not both. Only one ground connection is required.

&nbsp;

### Software Setup

Check out the original article 
[Adding a secondary sd card on Raspberry Pi](https://ralimtek.com/posts/2016/2016-12-10-raspberry_pi_secondary_sd_card/) 
by Ben V. Brown where he walks through the steps of setting up a secondary sd card for a raspberry pi zero.
In addition, there are extra steps for using older models of the raspberry pi or compute modules.


1. To begin, first enable SPI on the raspberry device by entering `sudo raspi-config` and navigate to `Interface Options`
and then to `SPI` where you can select 'Yes', followed by a reboot:
```shell
sudo shutdown -r now
```


2. To begin ensure the system is up-to-date including the device tree compiler (on newer systems it comes preinstalled):
```shell
sudo apt update && sudo apt full-upgrade
sudo apt install device-tree-compiler
```

2. Next, create and edit the file *mmc_spi.dts*. Use any editor you like, I used `nano`.
```shell
nano mmc_spi.dts
```

3. Insert the following into the new file. (Note: this is for CS 0 and works only for a single sd card, 
check out the original article for information on two sd cards.)
```text
/dts-v1/;
/plugin/;

/ {
   compatible = "brcm,bcm2835", "brcm,bcm2836", "brcm,bcm2708", "brcm,bcm2709";

   fragment@0 {
      target = <&spi0>;
      frag0: __overlay__ {
         status = "okay";
         sd1 {
                reg = <0>;
                status = "okay";
                compatible = "spi,mmc_spi";
                voltage-ranges = <3000 3500>;
                spi-max-frequency = <8000000>;
         };
      };
   };
};
```

4. Compile the created device tree source file:
```shell
dtc -@ -I dts -O dtb -o mmc_spi.dtbo mmc_spi.dts
```

5. To enable the system to use this file, copy it to the `/boot/overlays/` directory:
```shell
sudo cp mmc_spi.dtbo /boot/overlays/
```

6. Next, we need to tell the system to load the overlay automatically. To do so edit the device config using root
permissions and add the line `dtoverlay=mmc_spi` at the end of the file. After this reboot the system and we can start
looking for sd cards over spi.
```shell
sudo nano /boot/config.txt
```

7. Plug in a sd card if it isn't already and check if it's showing up on the system (may require formatting) 
using the command below. (Note: the boot ssd usually appears as `mmcblk0` and `mmcblk0p1`, any additional sd cards 
added should appear as `mmcblk1, 2, ... ,some number`)
```shell
ls /dev/mmc*
```

## Creating Raspberry Pi Backup Images

Throughout development, it is often useful to back up the raspbian operating systems as progress has been made. I have
found myself in many situations in which I have seriously messed something up and have to repeat everything I have done
thus far to catch back up. Saving different versions of the system using a versioning technique such as V0.1.0, can be
highly beneficial even for future projects.

### Linux

1. Remove the sd card form the raspberry pi and insert into your computer or card reader. Open the terminal and enter
`sudo fdisk -l` to list all the filesystems present on your system.

2. Using your sd card size try to find the name of your device, often `/dev/sdb` with a slightly smaller storage size
than what the card actually lists. **Note down this device name**.

3. Use the `dd` command to write the image to your systems hard drive for example:
```shell
sudo dd if=/dev/sdb of=~/raspbian_backup.img
```
The *if* parameter refers to the input file(replace with the name of your device) and the *of* parameter refers to the 
output file with the location and name of the backup file.
> Note: double-check your parameters before executing the `dd` command as entering incorrect parameters can potentially 
> data on your drives.

4. There may not be any output from the command above until the cloning is complete and at this point you can remove the
sd card and and place it back in the raspberry pi.

### macOS

1. Remove the sd card form the raspberry pi and insert into your computer or card reader. Open the terminal and enter
`diskutil list` to list all the filesystems present on your system.

2. Using your sd card size try to find the name of your device, often `/dev/disk3` with a slightly smaller storage size
than what the card actually lists. **Note down this device name**.

3. Next, unmount you sd card using the name of you sd card found previously:
```shell
diskutil unmountDisk /dev/disk3
```

5. Use the `dd` command to write the image to your systems hard drive for example:
```shell
sudo dd if=/dev/sdb of=~/raspbian_backup.img
```
The *if* parameter refers to the input file(replace with the name of your device) and the *of* parameter refers to the 
output file with the location and name of the backup file.
> Note: double-check your parameters before executing the `dd` command as entering incorrect parameters can potentially 
> data on your drives.

4. There may not be any output from the command above until the cloning is complete and at this point you can remove the
sd card and and place it back in the raspberry pi.