import pyudev

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')


def log_event(action, device):
    if 'ID_FS_TYPE' in device:
        with open('filesystems.log', 'a+') as stream:
            print('{0} - {1}'.format(action, device.get('ID_FS_LABEL')), file=stream)


observer = pyudev.MonitorObserver(monitor, log_event)
observer.start()
