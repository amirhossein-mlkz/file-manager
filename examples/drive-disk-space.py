import diskManager

mydisk = diskManager.diskMemory('c:\\')
print('free disk space: {} GB'.format(mydisk.free.toGB()))
print('used disk space: {} %'.format(mydisk.used.toPercent()))
print('total disk space: {} GB'.format(mydisk.total.toGB()))

