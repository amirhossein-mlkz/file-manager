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


## fileManager
fileManager do actions like copy file when some condition happend. to use this class, you need define your custom condition function that get a fileManager instance  as input and return True when your Ideal conditions happend. you can also use some predefined condition. let look at this example:
in this example we want remove a file, if it is an image

### step1:
define your condition function. you can use pre defineds 
``` python
import diskManager
from diskManager import FileCondition, FileManager, FileAction, File

def mycustom_condition(file:diskManager.File):
    be_image = FileCondition.file_extention('in', ['jpg', 'png'])
    # you can Also Write
    #       be_image = FileCondition.file_extention(diskManager.Conditions.contain, ['jpg', 'png'])
    
    return be_image(file)#it return True if condition occurd
```
### step2:
define your fileManager. you can add multiple operation with diffrents Action and condition 
``` python
# build your file manager
fm = FileManager()
fm.add_operation( mycustom_condition, FileAction.delete())
```

### step3:
run your fileManager on your files
``` python
#-----------------------
#load your file
myfile = diskManager.File('examples/test-folder\steve-jobs-black-and-white.jpg')
#-----------------------
#do your operations on your file
fm.set_file(myfile)
fm.run()

```
