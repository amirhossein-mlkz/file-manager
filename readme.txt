# file-manager

## diskMemory
diskMemory is used for find out disk space by:

```python
import diskManager

mydisk = diskManager.diskMemory('c:\\')
print('free disk space: {} GB'.format(mydisk.free.toGB()))
print('used disk space: {} %'.format(mydisk.used.toPercent()))
print('total disk space: {} GB'.format(mydisk.total.toGB()))
```
## File
File Class show all file info like name and creation time. it also has some method like is_file to check is file or folder
```python
import diskManager

file = diskManager.File('examples/test-folder\steve-jobs-black-and-white.jpg')
print(file.is_folder())
print(f'file size is: {file.parms.size().toKB()} KB')
print(f'file extention is: {file.parms.extention()}')
```
all parms are:
  