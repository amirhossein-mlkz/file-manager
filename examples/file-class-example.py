import diskManager

file = diskManager.File('examples/test-folder\steve-jobs-black-and-white.jpg')
print(file.is_folder())
print(f'file size is: {file.parms.size().toKB()} KB')
print(f'file extention is: {file.parms.extention()}')