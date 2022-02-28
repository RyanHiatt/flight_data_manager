import pyudev
import psutil

context = pyudev.Context()

removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
for device in removable:
    partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
    print("All removable partitions: {}".format(", ".join(partitions)))
    print("Mounted removable partitions:")
    for p in psutil.disk_partitions():
        if p.device in partitions:
            print("  {}: {}".format(p.device, p.mountpoint))
