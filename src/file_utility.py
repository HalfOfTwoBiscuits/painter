from os import path
class FileUtility:
    '''Class used to load game resource files.'''
    __RESOURCES_DIRNAME = 'resources'

    # This file is in the src directory
    __SRC_DIR = path.dirname(path.abspath(__file__))
    
    # Go up one level and add 'resources' to find the
    # resources directory.
    __RESOURCES_DIR = path.join(
        path.split(__SRC_DIR)[0], __RESOURCES_DIRNAME)
    
    # Resource folder names to the extentions of files in those folders
    __EXTENTIONS = {
        'sfx' : '.ogg',
        'font' : '.ttf',
        'floors' : '.yaml'
    }
    
    @classmethod
    def path_to_resource(cls, resource_type: str, filename: str):
        '''Given the type of a resource (the name of the directory it is in)
        and its filename without extention, return the absolute path to the file.
        The extention to use is determined by the resource type.'''

        extention = cls.__EXTENTIONS.get(resource_type, '')
        return path.join(cls.__RESOURCES_DIR, resource_type, filename + extention)
    
    @classmethod
    def path_to_resource_directory(cls, resource_type: str):
        '''Given a the name of a subdirectory for a type of resource,
        return the absolute path to that directory.'''
        return path.join(cls.__RESOURCES_DIR, resource_type)