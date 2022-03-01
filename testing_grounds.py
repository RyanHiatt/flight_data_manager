import pyudev
import psutil

context = pyudev.Context()


devices = [device for device in context.list_devices(subsystem="block", DEVTYPE="partition")]

for device in devices:
    print(device.device_node)

for part in psutil.disk_partitions():
    print(part)


# removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk')]
# for device in removable:
#     partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
#     print("All removable partitions: {}".format(", ".join(partitions)))
#     print("Mounted removable partitions:")
#     for p in psutil.disk_partitions():
#         if p.device in partitions:
#             print("  {}: {}".format(p.device, p.mountpoint))
