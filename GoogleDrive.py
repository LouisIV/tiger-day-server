from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import config


class GoogleDriveManager():
    def __init__(self):
        self.__is_authorized = False
        self.gauth = None
        self.drive = None

    def authorize(self):
        self.gauth = GoogleAuth(
            settings_file=config.SETTINGS_FILE
        )
        self.__is_authorized = True

    def create_drive_object(self):
        if self.__is_authorized:
            self.drive = GoogleDrive(self.gauth)
        else:
            self.authorize()
            self.create_drive_object()

    def get_root_directory(self):
        if self.drive:
            return self.drive.ListFile(
                {'q': "'root' in parents and trashed=false"}
            ).GetList()
        else:
            self.create_drive_object()
            return self.get_root_directory()

    def find_existing_file(self, query_title=None, query_id=None):

        if query_title is None and query_id is None:
            return False

        # Auto-iterate through all files in the root folder.
        file_list = self.get_root_directory()

        for file_object in file_list:
            if query_title and query_id:
                if file_object['title'] == query_title \
                   and file_object['id'] == query_id:
                    return self.create_file(file_id=file_object['id'])
            elif query_id:
                if file_object['id'] == query_id:
                    return self.create_file(file_id=file_object['id'])
            elif query_title:
                if file_object['title'] == query_title:
                    return self.create_file(file_id=file_object['id'])
        return False

    def create_file(self, title=False, file_id=False, upload=False):
        if not title and not file_id:
            return False

        if self.drive:
            if title:
                new_file = self.drive.CreateFile(
                    {'title': title, 'mimeType': 'application/json'}
                )
                if upload:
                    self.upload_file(new_file)
                return new_file
            elif file_id:
                new_file = self.drive.CreateFile(
                    {'id': file_id}
                )
                if upload:
                    self.upload_file(new_file)
                return new_file

        else:
            self.create_drive_object()
            return self.create_file(title, file_id, upload)

    def search_first(self, query_title=None, query_id=None):
        """Creates a file if it does not exist or returns the existing file
            Returns the `resulting_file` or a new file with the correct title.
        """
        resulting_file = self.find_existing_file(
            query_title=query_title, query_id=query_id
        )

        if resulting_file:
            return resulting_file
        else:
            return self.create_file(title=query_title, upload=True)

    def write_to_file(self, file_to_write, data, upload=False):
        """Writes to a given file"""
        if self.drive:
            # Set content of the file from given string.
            file_to_write.SetContentString(data)
            if upload:
                self.upload_file(file_to_write)
            return file_to_write
        else:
            self.create_drive_object()
            return self.write_to_file(file_to_write, data, upload)

    def upload_file(self, file_to_upload):
        """Uploads a file to the google drive"""
        if self.drive:
            file_to_upload.Upload()
        else:
            self.create_drive_object()
            self.upload_file(file_to_upload)
