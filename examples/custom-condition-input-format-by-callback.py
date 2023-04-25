import diskManager
from diskManager import FileCondition, FileManager, FileAction, File

def mycallback(filename):
    # for e.g. convert '2022-img.jpg' to 2022
    year = int(filename[:4])
    return year


def image_newer_2019_condition(file:diskManager.File):
    be_image = FileCondition.file_extention('in', ['jpg', 'png'])
    check_name_year = FileCondition.file_name('>', 2019, mycallback)
    
    return be_image(file) and check_name_year(file)


# build your file manager
fm = FileManager()
fm.add_operation( condition = image_newer_2019_condition,
                  true_action = FileAction.copy('examples\\test-folder\\after 2019'),
                  false_action = FileAction.copy('examples\\test-folder\\befor 2019'))
#-----------------------
#load your file
for path in ['examples/test-folder/2022-img.jpg', 
             'examples/test-folder/2017-img.png']:
    myfile = File(path)
    #-----------------------
    #do your operations on your file
    fm.set_file(myfile)
    fm.run()

print(fm.log)