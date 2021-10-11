# https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py
from __future__ import print_function
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.service_account import ServiceAccountCredentials
import os.path
import os
import six

from googleapiclient.discovery import build
import oauth2client.client
import shutil

CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/drive']


def authentication(scope = ['https://www.googleapis.com/auth/drive'], secrets_file='client_secrets.json'):
    gauth = GoogleAuth()
    flow = oauth2client.client.flow_from_clientsecrets(
        secrets_file, scope)
    flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
    authorize_url = flow.step1_get_authorize_url()
    print('Go to the following link in your browser: ' + authorize_url)
    code = six.moves.input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)

    gauth.credentials = credentials
    return GoogleDrive(gauth)


def create_folder(service, folder_name, id_parent):
    # Create folder
    folder_metadata = {
        'title': folder_name,
        # The mimetype defines this new file as a folder, so don't change this.
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': id_parent}]
    }
    folder = service.CreateFile(folder_metadata)
    folder.Upload()
    return folder  # get id and name: folder['id'], folder['title']


def upload_file(service, file_name, id_parent):
    file_metadata = {
        'title': file_name.split("/")[-1],
        'parents': [{'id': id_parent}]
        }

    file = service.CreateFile(file_metadata)
    file.SetContentFile(file_name)
    file.Upload()
    print("Uploaded: ", file_name)

def list_folder(service, id_parent):
    meta_data = {
        "q": " '{}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false".format(id_parent),
        # 'parents': [{'id': id_parent}]
    }
    f = service.ListFile(meta_data).GetList()
    # for folder in f:
    #     print(folder['title'])
    # return folder['title'], folder['id']
    return f

def zip_folder(output_filename, dir_name):
    shutil.make_archive(output_filename, 'zip', dir_name)

id_parent = "1m1tGsd0N4kCrv7n5Zb6Pt4JXGAY4wUro"

path_file = "hello.txt"
upload_file(service, path_file, id_parent)



