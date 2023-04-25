import diskManager
from diskManager import FileCondition, FileManager, FileAction, Scanner


def be_image(file:diskManager.File):
    be_image = FileCondition.file_extention('in', ['jpg', 'png'])
    return be_image(file)


fm = FileManager()
fm.add_operation( condition = be_image,
                  true_action = FileAction.copy('examples\\test-folder\\images only'))
#-----------------------

my_scanner = Scanner(fm)
my_scanner.scan(path='examples\\test-folder', deep=0)