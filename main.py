import argparse
import sqlite3
import os
import shutil
import subprocess
import shlex

BACKUP_DIRECTORY = "~/Library/Application Support/MobileSync/Backup/"
BACKUP_DIRECTORY = os.path.expanduser(BACKUP_DIRECTORY)

class File():
    fileID = None
    domain = None
    relativePath = None
    flags = None
    file = None
    
    def __init__(self, fileID, domain, relativePath,flags, file ) -> None:
        self.fileID = fileID
        self.domain = domain 
        self.relativePath = relativePath
        self.flags = flags
        self.file = file

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
    print(len(files), vars(files[-1]))
    
parser = argparse.ArgumentParser()

parser.add_argument("-b", "--backup_directory", type=str, default=get_default_backup_directory())
parser.add_argument("-d", "--destination_directory", type=str, default=None)
parser.add_argument("-e", "--extensions", type=list)
args = vars(parser.parse_args())

extract_media(**args)
