import argparse
import sqlite3
import os
import shutil
import subprocess
from enum import Enum

BACKUP_DIRECTORY = "~/Library/Application Support/MobileSync/Backup/"
BACKUP_DIRECTORY = os.path.expanduser(BACKUP_DIRECTORY)

class Domain(str, Enum):
    ALL = "all"
    FILES = "AppDomainGroup-group.com.apple.FileProvider.LocalStorage"
    MEDIA = "MediaDomain"
    BOOKS = "AppDomain-com.apple.iBooks"
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
    
    def move_file(self, backup_directory:str, output_directory:str):
        os.makedirs(output_directory, exist_ok=True)
        
        sub_directory = self.fileID[:2]
        
        source_path = os.path.abspath(os.path.join(backup_directory, sub_directory, self.fileID))
        destination_path = os.path.abspath(os.path.join(output_directory, self.file_name))
        
        try:
            if os.path.exists(source_path):  # Check if source file exists
                subprocess.run(["cp", source_path, destination_path], check=True)
                print(f"Copied {source_path} to {destination_path}.")
            else:
                print(f"Source file not found: {source_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error copying {source_path} to {destination_path}: {e}")
        
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

def get_files(database: str, domains: list = None, extensions: list = None):
    conn = sqlite3.connect(database)
    
    if domains:
        placeholders = ','.join(['?'] * len(domains))
        query = f"SELECT * FROM Files WHERE domain IN ({placeholders})"
        params = domains
    else:
        query = "SELECT * FROM Files"
        params = []
    
    try:
        cursor = conn.execute(query, params)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        return []

    files = [
        file for file in map_sqlite_results_to_objects(results, File)
        if not extensions or file.extension in extensions
    ]
    
    return files

def extract_media(backup_directory:str, output_directory:str = None, domains:list = None,extensions:list = None, remove_backup:bool = False):
    
    if domains and Domain.ALL in domains:
        domains = None
        
    if not os.path.isdir(backup_directory): # this is not a valid director, so it must be a name
        backup_directory = os.path.join(BACKUP_DIRECTORY,backup_directory)
    
    # make a connection to the .sql file within the backup directory
    database = os.path.join(backup_directory, 'Manifest.db')
    
    if not os.path.exists(database):
        raise FileNotFoundError("Manifest.db file not found.")
    
    files = get_files(database, domains, extensions)
    
    for file in files:
        file.move_file(backup_directory,output_directory)
    
    if remove_backup:
        shutil.rmtree(backup_directory)


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

parser = argparse.ArgumentParser()

parser.add_argument("-b", "--backup_directory", type=str, default=get_default_backup_directory())
parser.add_argument("-o", "--output_directory", type=str, default=desktop_path) # moves to desktop directory by default
parser.add_argument("-d", "--domains", nargs="?", default=[Domain.FILES])
parser.add_argument("-e", "--extensions", nargs="+")
parser.add_argument("-r", "--remove_backup", type=bool,default=False)

args = vars(parser.parse_args())

extract_media(**args)
