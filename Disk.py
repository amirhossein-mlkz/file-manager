

import shutil
import numpy as np
import os
from datetime import datetime
from datetime import timedelta

#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________
class Space:
    def __init__(self, byte, total_byte=-1):
        self.byte = byte
        self.total_byte = total_byte
    def toGB(self,):
        return self.byte / 1e9

    def toMB(self,):
        return self.byte / 1e6
    
    def toKB(self,):
        return self.byte /1e3
    
    def toPercent(self):
        return round(self.byte/self.total_byte, 3)*100

#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________
class diskMemory():

    def __init__(self,path):
        self.path = path
        self.refresh()
    

    def refresh(self):
        self.disk_size_info = shutil.disk_usage(self.path)
        self.used = Space(self.disk_size_info.used, self.disk_size_info.total)
        self.total = Space(self.disk_size_info.total, self.disk_size_info.total)
        self.free = Space(self.disk_size_info.free, self.disk_size_info.total)

#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________
class fileParms:

    def __init__(self,path):
        self._path = path
        self._file_extention = None
        self._full_name = None
        self._file_name = None
        self._dir = None
        self._creation_date = None
        self._size = None
        self._lifetime = None


    #---------------------------------------------------------------------
    def __extract_names_info__(self,):
        if self._full_name is None:
            self._full_name = os.path.basename(self._path)
            dot_loc = self._full_name.find('.')
            if dot_loc>=0:
                self._file_extention = self._full_name[ dot_loc + 1 :]
                self._file_name = self._full_name[ : dot_loc]
            else:
                self._file_extention = ''
                self._file_name = self._full_name

    #---------------------------------------------------------------------
    def __dir_size__(self, path):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.__dir_size__(entry.path)
        return total
    #---------------------------------------------------------------------
    def path(self):
        return self._path

    def name(self):
        self.__extract_names_info__()
        return self._file_name
    
    def extention(self):
        self.__extract_names_info__()
        return self._file_extention

    def full_name(self):
        self.__extract_names_info__()
        return self._full_name


    def dir(self):
        if self._dir is None:
            self._dir = os.path.dirname(self._path)
        return self._dir
    

    def creation_date(self):
        if self._creation_date is None:
            self._creation_date = datetime.fromtimestamp(os.path.getctime(self._path))
        return self._creation_date
    

    def size(self) -> Space:
        self.__extract_names_info__()
        if self._file_extention == '':
            self._size = Space(self.__dir_size__(self._path))
        else:
            self._size = Space(os.path.getsize( self._path ))
        return self._size
    

    def lifetime(self) -> datetime:
        self.creation_date()
        if self._lifetime is None:
            self._lifetime = datetime.today() - self.creation_date()
        return self._lifetime
    

    

#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________

class FileAction:
    @staticmethod
    def move( res_path):
        def _move_(file:File):
            shutil.move(file.parms.path(), res_path)
        return _move_

    @staticmethod
    def copy( res_path):
        def _copy_(file:File):
            shutil.copy(file.parms.path(), res_path)
        return _copy_

    @staticmethod
    def delete():
        def _delete_(file:File):
            if file.is_folder():
                shutil.rmtree(file.parms.path())
            else:
                os.remove(file.parms.path())
        return _delete_
#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________
class File:    
    def __init__(self, path):
        self.path = path
        self.parms = fileParms(self.path)


    def is_folder(self):
        return os.path.isdir(self.parms.path())



class FileManager:
    def __init__(self):
        self.file = None
        #self.actions = FileAction()
        self.operations = []

    def set_file(self, file:File):
        self.file = file

    def add_operation(self, condition, action ):
        opr = {'condition':condition, 'action':action}
        self.operations.append(opr)
    
    def run(self):
        assert self.file is not None, 'set a file before run'
        for opr in self.operations:
            if opr['condition'](self.file):
                opr['action'](self.file)










#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________





class Conditions:
    @staticmethod
    def bigger( parm , value):
        if parm > value:
            return True
        return False
    
    @staticmethod
    def samaller( parm , value):
        if parm < value:
            return True
        return False
    
    @staticmethod
    def bigger_and_equal( parm , value):
        if parm >= value:
            return True
        return False

    @staticmethod
    def samaller_and_equal( parm , value):
        if parm <= value:
            return True
        return False
    
    @staticmethod
    def samaller( parm , value):
        if parm < value:
            return True
        return False
    
    @staticmethod
    def equal( parm , value):
        if parm == value:
            return True
        return False
    
    def not_equal( parm , value):
        if parm != value:
            return True
        return False
    

    @staticmethod
    def contain( parm , value):
        if parm in value:
            return True
        return False
    
    @staticmethod
    def not_contain( parm , value):
        if parm not in value:
            return True
        return False
    



class FileCondition:
    #--------------------------------------------------------------
    @staticmethod
    def __append_calback__( inpt, func):
        if func is not None:
            return func(inpt)
        return inpt

    @staticmethod
    def condition(cond_type, value, input_callback=None):
        def func(inpt):
            inpt = FileCondition.__append_calback__(inpt, input_callback)
            return cond_type( inpt , value )
        return func

    #--------------------------------------------------------------
    @staticmethod
    def creation_time(cond_type, dt, input_callback=None):
        def func(file:File):
            inpt = FileCondition.__append_calback__(file.parms.creation_date(), input_callback)
            return cond_type( inpt , dt )
        return func

    #--------------------------------------------------------------
    @staticmethod
    def file_extention_is(cond_type, ex, input_callback = None):
        assert '.' not in ex, 'input extention without (.) char'
        def func(file:File):
            inpt = FileCondition.__append_calback__(file.parms.extention(), input_callback)
            return cond_type( inpt , ex )
        return func

    #--------------------------------------------------------------
    @staticmethod
    def file_lifetime(cond_type, age:datetime, input_callback = None):
        def func(file:File):
            inpt = FileCondition.__append_calback__(file.parms.lifetime(), input_callback)
            return cond_type( inpt , age )
        return func


    #--------------------------------------------------------------
    def file_name_is(file:File, name):
        pass


#____________________________________________________________________________________________________________________________________
#
#
#____________________________________________________________________________________________________________________________________
def condition(file:File):
        try:
            if int(file.parms.name()) > 2022:
                return True
            return False
        except:
            return False


condition
#disk_size_info = list(map( lambda x:x/1024000000, disk_size_info ))
dm = diskMemory('c:\\')
main_path = 'files'
f = File('files\steve-jobs-black-and-white.jpg')
#func_life_time = FileCondition.file_lifetime(Conditions.bigger, timedelta(hours=1))
#func_life_time(f)

fm = FileManager()
fm.add_operation(condition, FileAction.delete())
for fname in os.listdir(main_path):
    path = os.path.join(main_path, fname)
    my_file = File(path)
    fm.set_file(my_file)
    fm.run()
#fm = File()




print(dm.used.toPercent())
print(os.path.dirname('ami/123/digi'))

'''

if condtion(file) ->  action(copy):


[ [  x1 or x2 ] and [x]  ]

'''