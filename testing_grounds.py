import pyudev

context = pyudev.Context()


for device in context.list_devices(subsystem='block'):
    print('{0} ({1})'.format(device.device_node, device.device_type))
