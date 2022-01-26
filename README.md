# Flight Data Retrieval and Management System

### Table of Contents
- [Interfacing the SD Card Module](https://github.com/RyanHiatt/flight_data_manager#interfacing-the-sd-card-module)
    - [Wiring](https://github.com/RyanHiatt/flight_data_manager#wiring)
    - [Software](https://github.com/RyanHiatt/flight_data_manager#software)




## Interfacing the SD Card Module

For this project flight data is accumulated to a full size sd card, however the raspberry pi doesn't have support for a
full size sd card. One option would be to use a USB dongle, but taking into consideration aesthetics and having the
ability to build a sd card reader into the device enclosure, I opted for a sd card module using SPI.

[![SD Card Module](/static/images/sd_card_module.png)](https://www.amazon.com/dp/B07XGQ863W?psc=1&ref=ppx_yo2_dt_b_product_details)

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
<img style="float: right;" src="/static/images/raspberry_pi_4_pinout.png">

> Note: Use either 3V3 or 5V the module supports either one but not both. Only one ground connection is required.

[![Raspberry Pi 4B Pinout ><](/static/images/raspberry_pi_4_pinout.png)](https://www.raspberrypi.com/documentation/computers/os.html)

<img style="float: center;" src="/static/images/raspberry_pi_4_pinout.png">

### Software

Check out the original article [Adding a secondary sd card on Raspberry Pi](https://ralimtek.com/posts/2016/2016-12-10-raspberry_pi_secondary_sd_card/) 
by Ben V. Brown where he walks through the steps of setting up a secondary sd card for a raspberry pi zero.

```shell
sudo apt update && sudo apt full-upgrade
```

```shell
nano mmc_spi.dts
```


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

```shell
dtc -@ -I dts -O dtb -o mmc_spi.dtbo mmc_spi.dts
```


```shell
sudo cp mmc_spi.dtbo /boot/overlays/
```


```shell
sudo nano /boot/config.txt
```


