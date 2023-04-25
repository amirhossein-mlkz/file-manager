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
```
free disk space: 29.533495296 GB
used disk space: 88.2 %
total disk space: 249.400651776 GB
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

```
False
file size is: 66.587 KB
file extention is: jpg
```


all method in parms are:
* path() -> file or folder path
* name() -> file or folder name without extention
* extention() -> file extention, for folder it is empty string ''
* full_name() -> name via extention
* dir() -> direction
* creation_date() -> date that file or folder created
* size() -> file size, for folder it calculated sumb of all sub files and sub folders
* lifetime() -> age of file from now
