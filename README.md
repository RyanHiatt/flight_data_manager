# Flight Data Retrieval and Management System

### Table of Contents
- [Interfacing the SD Card Module](https://github.com/RyanHiatt/flight_data_manager#interfacing-the-sd-card-module)
    - [Wiring](https://github.com/RyanHiatt/flight_data_manager#wiring)
    - [Software Setup](https://github.com/RyanHiatt/flight_data_manager#software-setup)




## Interfacing the SD Card Module

For this project flight data is accumulated to a full size sd card, however the raspberry pi doesn't have support for a
full size sd card. One option would be to use a USB dongle, but taking into consideration aesthetics and having the
ability to build a sd card reader into the device enclosure. I opted for a sd card module using SPI.

[![SD Card Module](/static/images/sd_card_module.png)](https://www.amazon.com/dp/B07XGQ863W?psc=1&ref=ppx_yo2_dt_b_product_details)

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


1. To begin ensure the system is up-to-date including the device tree compiler (on newer systems it comes preinstalled):
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


