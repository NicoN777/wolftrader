from azure.storage.fileshare import ShareClient
from application import azure_store_account_name, azure_store_connstr
from util.logger import *


class FileStore:
    def __init__(self, account_name, connection_str):
        self.__account_name = account_name
        self.__connection_str = connection_str
        self.share_client = ShareClient.from_connection_string(self.__connection_str, 'wolfiefs')
        # self.share_client.create_share()
        self.directory_client = self.share_client.get_directory_client()
        self.share_properties = self.share_client.get_share_properties()

    def upload(self, source, filename):
        """
        :param str source: Full path and filename of the file you want to upload
        :param str filename: Name for the file
        :return: None
        """
        try:
            file_in = self.share_client.get_file_client(filename)
            with open(source, 'rb') as s:
                file_in.upload_file(s)
            log_info(f'{__file__} file: {filename} uploaded')
        except Exception as e:
            log_critical(f'{__file__} error uploading file, got {e}')

    def download(self, filename, destination):
        """
        :param str filename: The name of target file you want to download
        :param str destination: Full path where file should be written
        :return: None
        """
        try:
            file_out = self.share_client.get_file_client(file_name=filename)
            with open(destination, 'wb') as d:
                stream = file_out.download_file()
                d.write(stream.readall())
            log_info(f'{__file__} file: {destination} uploaded')
        except Exception as e:
            log_critical(f'{__file__} error uploading file, got {e}')

    def all_file_properties(self, creation_date_filter=None, operator='after'):
        """
        :param operator:
        :param :
        :param datetime creation_date_filter: Get file properties for
                those who are greater than date specified
        :return:
        """
        files_properties = (self.share_client.get_file_client(file['name']).get_file_properties()
                      for file in self.share_client.list_directories_and_files())

        if creation_date_filter:
            func = lambda file_property: file_property.creation_date > creation_date_filter
            if operator == 'before':
                func = lambda file_property: file_property.creation_date < creation_date_filter
            filtered = filter(func, files_properties)
            return filtered
        else:
            return files_properties

    def __repr__(self):
        return f'FileStore(<account_name>,<connection_string>)'


if __name__ == '__main__':
    fs = FileStore(azure_store_account_name, azure_store_connstr)
    print(fs)
    import os
    cwd = os.getcwd()
    destination = 'data_massage.py'
    source = os.path.join(cwd, destination)
    for _ in fs.all_file_properties():
        print(_)
    print('...')