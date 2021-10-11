from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.service_account import ServiceAccountCredentials
import os.path
import os
import six
from googleapiclient.discovery import build
import oauth2client.client
import shutil


class DriveAPI:
    def __init__(self, client_secret_file, scopes,) -> None:
        self.__client_secret_file = client_secret_file
        self._scope = scopes
        self.service = None
        self.credentials = None

    def authenticate(self):
        flow = oauth2client.client.flow_from_clientsecrets(
            self.__client_secret_file, self._scope)
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
        authorize_url = flow.step1_get_authorize_url()
        print('Go to the following link in your browser: ' + authorize_url)
        code = six.moves.input('Enter verification code: ').strip()
        self.credentials = flow.step2_exchange(code)

    def create_service(self):
        gauth = GoogleAuth()
        gauth.credentials = self.credentials
        self.service = GoogleDrive(gauth)
        print("SERVICE CREATED !!")

    def upload_file(self, file_name, id_parent):
        file_metadata = {
            'title': file_name.split("/")[-1],
            'parents': [{'id': id_parent}]
        }

        file = self.service.CreateFile(file_metadata)
        file.SetContentFile(file_name)
        file.Upload()
        print("Uploaded: ", file_name)

    def create_folder(self, dir_name, id_parent):
        folder_metadata = {
            'title': dir_name,
            # The mimetype defines this new file as a folder, so don't change this.
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': id_parent}]
        }

        folder = self.service.CreateFile(folder_metadata)
        folder.Upload()
        return folder  # folder['id'], folder['title']

    def list_folder_in_folder(self, id_parent):
        meta_data = {
            "q": " '{}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false".format(id_parent),
        }
        f = self.service.ListFile(meta_data).GetList()
        return f  # list folder
    
    def list_file(self, id_parent):
        meta_data = {
            "q": " '{}' in parents and mimeType='application/vnd.google-apps.file' ".format(id_parent),
        }
        f = self.service.ListFile(meta_data).GetList()
        return f

    def download_file(self, id_file, path_file_local, name_file=None):
        file = self.CreateFile({'id': id_file})
        print('Downloading file %s from Google Drive' % file['title']) # 'hello.png'
        if name_file == None:
            name_file = file['title']
        file.GetContentFile(os.path.join(path_file_local, name_file))  # Save Drive file as a local file
    
    @staticmethod
    def zip_folder(output_filename, dir_name):
        shutil.make_archive(output_filename, 'zip', dir_name)
        print("Zip folder success!")