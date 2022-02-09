# Flight Data Retrieval and Management System

## Project Overview

### Table of Contents

- [Installing Kivy 2.0.0 on Raspberry Pi](https://github.com/RyanHiatt/flight_data_manager#installing-kivy-200-on-raspberry-pi-headless)
  - [Enable Using Official RPi Touch Display](https://github.com/RyanHiatt/flight_data_manager#enable-using-official-rpi-touch-display)
- [Geekworm X735 V2.5 Shield Installation](https://github.com/RyanHiatt/flight_data_manager#geekworm-x735-v25-shield-installation)
  - [Installation](https://github.com/RyanHiatt/flight_data_manager#installation)
  - [Software](https://github.com/RyanHiatt/flight_data_manager#software)
- [Connecting the Official Raspberry Pi 7in Touchscreen](https://github.com/RyanHiatt/flight_data_manager#connecting-the-official-raspberry-pi-7in-touchscreen)
- [Interfacing the SD Card Module](https://github.com/RyanHiatt/flight_data_manager#interfacing-the-sd-card-module)
  - [Wiring](https://github.com/RyanHiatt/flight_data_manager#wiring)
  - [Software Setup](https://github.com/RyanHiatt/flight_data_manager#software-setup)
- [Creating Raspberry Pi Backup Images](https://github.com/RyanHiatt/flight_data_manager#creating-raspberry-pi-backup-images)
  - [Linux](https://github.com/RyanHiatt/flight_data_manager#linux)
  - [macOS](https://github.com/RyanHiatt/flight_data_manager#macos)
- [Drive Formatting, Partitioning, File Systems](https://github.com/RyanHiatt/flight_data_manager#drive-formatting-partitioning-file-systems)

___

## Installing Kivy 2.0.0 on Raspberry Pi Headless

The following are the origional documentation for the process of installing and running Kivy on a Raspberry Pi:
- [Installing Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html#kivy-source-install)
- [Kivy Installation on Raspberry Pi](https://kivy.org/doc/stable/installation/installation-rpi.html)

1. Before beginning, ensure your system is up-to-date, python and pip are installed, and also up-to-date:
```shell
sudo apt update && sudo apt upgrade
sudo apt install python3-setuptools git-core python3-dev
sudo apt install python-pip
python -m pip install --upgrade pip setuptools virtualenv
```

2. First install Kivy using pip:
```shell
python3 -m pip install kivy
```

3. Source installation dependencies
```shell
sudo apt update
sudo apt install pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   libgstreamer1.0-dev \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} libmtdev-dev \
   xclip xsel libjpeg-dev
```

4. SDL2 installation using headless environment:
   1. Install Requirements:
    ```shell
    sudo apt-get install libfreetype6-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev libudev-dev libasound2-dev liblzma-dev libjpeg-dev libtiff-dev libwebp-dev git build-essential
    sudo apt-get install gir1.2-ibus-1.0 libdbus-1-dev libegl1-mesa-dev libibus-1.0-5 libibus-1.0-dev libice-dev libsm-dev libsndio-dev libwayland-bin libwayland-dev libxi-dev libxinerama-dev libxkbcommon-dev libxrandr-dev libxss-dev libxt-dev libxv-dev x11proto-randr-dev x11proto-scrnsaver-dev x11proto-video-dev x11proto-xinerama-dev
    ```
   2. Install SDL2:
   ```shell
    wget https://libsdl.org/release/SDL2-2.0.10.tar.gz
    tar -zxvf SDL2-2.0.10.tar.gz
    pushd SDL2-2.0.10
    ./configure --enable-video-kmsdrm --disable-video-opengl --disable-video-x11 --disable-video-rpi
    make -j$(nproc)
    sudo make install
    popd
    ```
   3. Install SDL2_image:
   ```shell
    wget https://libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz
    tar -zxvf SDL2_image-2.0.5.tar.gz
    pushd SDL2_image-2.0.5
    ./configure
    make -j$(nproc)
    sudo make install
    popd
    ```
   4. Install SDL2_mixer:
   ```shell
    wget https://libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.4.tar.gz
    tar -zxvf SDL2_mixer-2.0.4.tar.gz
    pushd SDL2_mixer-2.0.4
    ./configure
    make -j$(nproc)
    sudo make install
    popd
    ```
   5. Install SDL2_ttf:
   ```shell
    wget https://libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz
    tar -zxvf SDL2_ttf-2.0.15.tar.gz
    pushd SDL2_ttf-2.0.15
    ./configure
    make -j$(nproc)
    sudo make install
    popd
    ```

5. Make sure the dynamic libraries caches is updated:
```shell
sudo ldconfig -v
```
If you are getting output similar to this when running your app:
```shell
[INFO   ] GL: OpenGL vendor <b'VMware, Inc.'>
[INFO   ] GL: OpenGL renderer <b'llvmpipe (LLVM 9.0.1, 128 bits)'>
```
Then it means that the renderer is NOT hardware accelerated. This can be fixed by adding your user to the render group:
```shell
sudo adduser "$USER" render
```
You will then see an output similar to this:
```shell
[INFO   ] GL: OpenGL vendor <b'Broadcom'>
[INFO   ] GL: OpenGL renderer <b'V3D 4.2'>
```

### Enable Using Official RPi Touch Display

To use the official Raspberry Pi Display, you need to configure Kivy to use it as an input source. To do this first run
a Kivy application to generate its config files then edit the file `nano ~/.kivy/config.ini` and go to the [input] 
section and match the following:
```shell
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

___

## Geekworm X735 V2.5 Shield Installation

[![Geekworm X735 V2.5 Shield](/static/images-github/geekworm_x735_v2-5.png)](https://www.amazon.com/Geekworm-Raspberry-Management-Expansion-Compatible/dp/B07R45W1LN/ref=pd_bxgy_img_2/147-1032413-0120637?pd_rd_w=GVGAz&pf_rd_p=6b3eefea-7b16-43e9-bc45-2e332cbf99da&pf_rd_r=N3J44B70SEC8CYZ6RK8T&pd_rd_r=0e130e86-118a-493c-8063-24000bf0cc8f&pd_rd_wg=ShFxX&pd_rd_i=B07R45W1LN&psc=1)

### Installation

Installation is extremely simple, just attach the shield to the Raspberry Pi using the included standoffs, ensuring
it is seated on the gpio pins.

### Software

#### Install

1. To begin ensure the system is up-to-date:
```shell
sudo apt update && sudo apt upgrade
```

2. Next, the following can be run line by line to install the required packages, 
clone the repository(I cloned mine in the 'home' repository), and give permissions:
```shell
python3 -m pip install smbus2
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
echo "alias fanspeed='python3 ~/x735-v2.5/read_fan_speed.py'" >> ~/.bashrc
```

#### Uninstall

To uninstall the scripts, cd into the scripts directory `cd x735-v2.5` and run:
```shell
sudo unistall.sh
```

___

## Connecting the Official Raspberry Pi 7in Touchscreen


___

## Interfacing the SD Card Module

For this project flight data is accumulated to a full size sd card, however the raspberry pi doesn't have support for a
full size sd card. One option would be to use a USB dongle, but taking into consideration aesthetics and having the
ability to build a sd card reader into the device enclosure. I opted for a sd card module using SPI.

[![SD Card Module](/static/images-github/sd_card_module.png)](https://www.amazon.com/dp/B07XGQ863W?psc=1&ref=ppx_yo2_dt_b_product_details)

&nbsp;

### Wiring

| SD Card Module  |     Raspberry Pi 4B     |   
|:---------------:|:-----------------------:|
|       GND       |      Not Connected      |
|       3V3       |   Pin 17 - 3V3 power    |
|       5V        |      Not Connected      |
|       CS        |  Pin 24 - GPIO 8 (CE0)  |
|      MOSI       | Pin 19 - GPIO 10 (MOSI) |
|       SCK       | Pin 23 - GPIO 11 (SCLK) |
|      MISO       | Pin 21 - GPIO 9 (MISO)  |
|       GND       |      Pin 25 - GRND      |


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

___

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

___

## Drive Formatting, Partitioning, File Systems

1. Before making a partition, list available storage devices and partitions. This action helps identify the storage 
device you want to partition. Run the following command with sudo to list storage devices and partitions:
```shell
sudo parted -l
```

2. Open the storage disk that you intend to partition by running the following command:
```shell
sudo parted /dev/sda
```

3. Create a partition table before partitioning the disk. A partition table is located at the start of a hard drive 
and it stores data about the size and location of each partition. Partition table types are: 
aix, amiga, bsd, dvh, gpt, mac, ms-dos, pc98, sun, and loop. The create a partition table, enter the following:
```shell
mklabel msdos
```

4. Run the print command to review the partition table. The output displays information about the storage device:
```shell
Model: ASMT 2115 (scsi)
Disk /dev/sda: 250GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags: 

Number  Start  End  Size  Type  File system  Flags
```

5. Now let’s make a new partition using the ntfs file system. The assigned disk start shall be 0% and the disk end is 
at 100%. To create a new partition, enter the following:
```shell
mkpart primary ntfs o% 100%
```
After that, run the print command to review information on the newly created partition. The information is 
displayed under the Disk Flags section:
```shell
(parted) print                                                            
Model: ASMT 2115 (scsi)
Disk /dev/sda: 250GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags: 

Number  Start   End    Size   Type     File system  Flags
 1      33.6MB  250GB  250GB  primary
```

6. To save your actions and quit, enter the quit command. Changes are saved automatically with this command:
```shell
quit
```

7. The drive has been formatted and a partition was made, lastly we need to create a filesystem in that partition:
```shell
sudo mkfs.ntfs /dev/sda1
```

8. Finally, the project script will mount this drive automatically when run, but if you want to mount it
manually enter the following:
```shell
sudo mkdir -p /home/pi/flight_data_manager/mount_points/hard_drive
sudo mount -t auto /dev/sda1 /home/pi/flight_data_manager/mount_points/hard_drive
```

9. Check the file system was mounted using `lsblk` which should output the following:
```shell
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 232.9G  0 disk 
└─sda1        8:1    0 232.8G  0 part /home/pi/flight_data_manager/mount_points/hard_drive
```
