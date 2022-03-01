import pyudev
import psutil
import time

context = pyudev.Context()


while True:
    devices = [device for device in context.list_devices(subsystem="block", DEVTYPE="partition")]
    for device in devices:
        # if "sda" in device.device_node:
        #     print("Hard drive detected")
        if "mmcblk" in device.device_node and "0" not in device.device_node:
            print("SD card detected")
        elif "sdb" in device.device_node:
            print("USB drive detected")
        else:
            print("no new devices")

# for device in devices:
#     print(device.device_node)
#
# for part in psutil.disk_partitions():
#     print(part.mountpoint)








# removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk')]
# for device in removable:
#     partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
#     print("All removable partitions: {}".format(", ".join(partitions)))
#     print("Mounted removable partitions:")
#     for p in psutil.disk_partitions():
#         if p.device in partitions:
#             print("  {}: {}".format(p.device, p.mountpoint))
