import argparse
import sqlite3
import os
import shutil
import subprocess
import shlex
from enum import Enum
BACKUP_DIRECTORY = "~/Library/Application Support/MobileSync/Backup/"
BACKUP_DIRECTORY = os.path.expanduser(BACKUP_DIRECTORY)

class Domain(str, Enum):
    FILES = "AppDomainGroup-group.com.apple.FileProvider.LocalStorage"
    # MUSIC = ""
    # MOVIES = ""
    # BOOKS = ""
    PHOTOS = "CameraRollDomain"
    
class File():
    fileID = None
    domain = None
    relativePath = None
    flags = None
    file = None
    
    extension = None
    size = None
    file_name = None
    
    def __init__(self, fileID, domain, relativePath,flags, file ) -> None:
        self.fileID = fileID
        self.domain = domain 
        self.relativePath = relativePath
        self.flags = flags
        self.file = file
    
    def move_file(self, destination_directory:str):
        pass
    
    @property
    def size(self):
        return len(self.file) if self.file else 0

    @property
    def extension(self):
        return os.path.splitext(self.relativePath)[1][1:]
    
    @property
    def file_name(self):
        return os.path.basename(self.relativePath)
    
    def __repr__(self) -> str:
        return f"<File fileID={self.fileID}, name={self.file_name}"
    
    
def get_default_backup_directory():
    default_backup_directory = os.path.join(os.getcwd(), "backup")
    default_backup_directory = os.path.join(default_backup_directory, os.listdir(default_backup_directory)[0])
    return default_backup_directory


def map_sqlite_results_to_objects(
    sqlite_results: list, object_type
):
    return [object_type(*row) for row in sqlite_results]

def extract_media(backup_directory:str, destination_directory:str = None, extensions:list = []):
    if not os.path.isdir(backup_directory): # this is not a valid director, so it must be a name
        backup_directory = os.path.join(BACKUP_DIRECTORY,backup_directory)
    
    # make a connection to the .sql file within the backup directory
    database = os.path.join(backup_directory, 'Manifest.db')
    
    if not os.path.exists(database):
        raise FileNotFoundError("Manifest.db file not found.")
    
    conn = sqlite3.connect(database)

    query = "SELECT * FROM Files WHERE domain = 'AppDomainGroup-group.com.apple.FileProvider.LocalStorage'"
    results = []
    try:
        cursor = conn.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        
    files = map_sqlite_results_to_objects(results, File)
    
    for file in files:
        print(file)
    
parser = argparse.ArgumentParser()

parser.add_argument("-b", "--backup_directory", type=str, default=get_default_backup_directory())
parser.add_argument("-d", "--destination_directory", type=str, default=None)
parser.add_argument("-d", "--domains", type=list, default=[Domain.FILES])
parser.add_argument("-e", "--extensions", type=list)
parser.add_argument("-r", "--remove_backup", type=bool,default=False)

args = vars(parser.parse_args())

extract_media(**args)
