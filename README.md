# file-manager

## diskMemory
is used to show disk space in KB, MB, GB, and percentage format:

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
File Class shows all file info like name and creation time. it also has some methods like is_file to check if the path is a file or a folder. it uses for both folder and file 

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
fileManager do actions like copy file when some condition happens. to use this class, you need to define your custom condition function that gets a fileManager instance as input and return True when your Ideal conditions happened. then you can define two actions that run if the condition is established or not. you can also use some predefined conditions. let's look at this example:
in this example we want to remove a file, if it is an image
### example 1
#### step1:
define your condition function. you can use pre-defined 
``` python
import diskManager
from diskManager import FileCondition, FileManager, FileAction, File

def mycustom_condition(file:diskManager.File):
    be_image = FileCondition.file_extention('in', ['jpg', 'png'])
    # you can Also Write
    #       be_image = FileCondition.file_extention(diskManager.Conditions.contain, ['jpg', 'png'])
    
    return be_image(file)#it return True if condition occurd
```
#### step2:
define your fileManager. you can add multiple operations with different Actions and condition. in this example, we only want an action to occur when the condition is established, so we only use the true_action argument
``` python
# build your file manager
fm = FileManager()
fm.add_operation( mycustom_condition, true_action=FileAction.delete())
```

#### step3:
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

if you need to customize input of predefined conditions, you can use condition callback, condition callback is a method that runs on input parameters before checking conditions.
### example2: input callback

in this example, our file's name is like ('2022-img.jpg') the first four characters represent the year and we want to copy files whose year is bigger than 2019. for this reason, we should customize our file's name and split 4 first characters, and convert it to a number. In such a situation, we can use input_callback.

#### step1:
first, we define our callback method that converts a file's name to the intended format
```python
def mycallback(filename):
    # for e.g. convert '2022-img.jpg' to 2022
    year = int(filename[:4])
    return year
```

#### step2:
now we define our condition function. for the FileCondition.file_name condition, we pass our callback to the function for converting the file's name to our ideal format:
```python
def image_newer_2019_condition(file:diskManager.File):
    be_image = FileCondition.file_extention('in', ['jpg', 'png'])
    check_name_year = FileCondition.file_name('>', 2019, mycallback)
    
    return be_image(file) and check_name_year(file)
```

#### step4:
now we define our FileManager. In this example, we want to copy images whose in their names are more than 2019 to the related folder and if not, copy them to another folder
```python
fm = FileManager()
fm.add_operation( condition = image_newer_2019_condition,
                  true_action = FileAction.copy('examples\\test-folder\\after 2019'),
                  false_action = FileAction.copy('examples\\test-folder\\befor 2019'))
```

#### step5:
now let's run the defined File Manager on our files
```python
for path in ['examples/test-folder/2022-img.jpg', 
             'examples/test-folder/2017-img.png']:
    myfile = File(path)
    #-----------------------
    #do your operations on your file
    fm.set_file(myfile)
    fm.run()

print(fm.log)
```
```
[['examples/test-folder/2022-img.jpg', '_copy_'],
 ['examples/test-folder/2017-img.png', '_copy_']]
```
