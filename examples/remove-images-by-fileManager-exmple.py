import diskManager
from diskManager import FileCondition, FileManager, FileAction, File

def mycustom_condition(file:diskManager.File):
    be_image = FileCondition.file_extention('in', ['jpg', 'png'])
    # you can Also Write
    #       be_image = FileCondition.file_extention(diskManager.Conditions.contain, ['jpg', 'png'])
    
    return be_image(file)#it return True if condition occurd

# build your file manager
fm = FileManager()
fm.add_operation( mycustom_condition, true_action=FileAction.delete())
#-----------------------
#load your file
myfile = diskManager.File('examples/test-folder\steve-jobs-black-and-white.jpg')
#-----------------------
#do your operations on your file
fm.set_file(myfile)
fm.run()