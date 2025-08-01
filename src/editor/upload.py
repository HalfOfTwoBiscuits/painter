import platform
from .editor_floor_manager import EditorFloorManager
class FloorpackUploader:
    __just_uploaded = False
    __aborting = False
    __upload_was_invalid = False
    __duplicate_name = None

    @classmethod
    def init(cls):
        '''Using JavaScript, set up an element on the web version's HTML page to
        recieve YAML file uploads, and call upload() on recieving a file.'''
        # This is a little hacky: writing JavaScript inside Python.
        # Apparently this is how pygbag does file upload.
            
        # Set python function to occur on uploading file
        platform.EventTarget.addEventListener(None, "upload", cls.__upload)
        # Change MIME type of upload element and change it so it doesn't accept multiple.
        # By default it is an image multi-upload.
        platform.window.dlg_multifile.accept = 'application/yaml'
        platform.window.dlg_multifile.multiple = false

    @classmethod
    def allow_upload(cls):
        '''Using JavaScript, make the input element for files on the web version's HTML page appear.'''
        platform.window.dlg.hidden = false
        cls.__aborting = False

    @staticmethod
    def remove_upload_prompt():
        '''Using JavaScript, make the input element for files on the web version's HTML page disappear.'''
        platform.window.dlg.hidden = true

    @classmethod
    def abort_upload(cls):
        '''If a file is currently being uploaded, there will be no effect when it finishes uploading.'''
        cls.__aborting = True

    @classmethod
    def __upload(cls, file_data):
        '''Loads the floorpack file with the path that's specified in the file_data namespace.
        Used when a file is uploaded.
        Does nothing if abort_upload() was called before this.'''
        if cls.__aborting:
            cls.__aborting = False
            return
        
        fname = file_data.name
        try:
            EditorFloorManager.upload_floorpack(file_data.text, fname)
        except TypeError:
            cls.__upload_was_invalid = True
        except FileExistsError:
            cls.__duplicate_name = EditorFloorManager.get_packname(fname)
        else:
            cls.__just_uploaded = True

    @classmethod
    def has_just_uploaded(cls) -> bool:
        '''Return True if the user successfully uploaded a file
        since this method was last called, False otherwise.'''
        if cls.__just_uploaded:
            cls.__just_uploaded = False
            return True
        else: return False

    @classmethod
    def upload_was_invalid(cls) -> bool:
        '''Return True if the user uploaded an invalid file
        since this method was last called, False otherwise.'''
        if cls.__upload_was_invalid:
            cls.__upload_was_invalid = False
            return True
        else: return False

    @classmethod
    def duplicate_name(cls) -> str | None:
        '''If the user uploaded a file with a duplicate name
        since this method was last called, return the name.
        Otherwise return None.'''
        duplicate_name = cls.__duplicate_name
        if duplicate_name is None:
            return None
        else:
            cls.__duplicate_name = None
            return duplicate_name