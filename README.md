# Interfacing the SD Card Module

![SD Card Module](/static/images/sd_card_module.png)

## Wiring

## Software

```shell
sudo apt update && sudo apt upgrade
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


