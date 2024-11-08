import argparse
import sqlite3
import os
import shutil
BACKUP_DIRECTORY = "/Library/Application Support/MobileSync/Backup"

def extract_media(backup_directory:str, destination_directory:str = None):
    os.path.isdir
    if not os.path.isdir(backup_directory): # this is not a valid director, so it must be a name
        backup_directory = os.path.join(BACKUP_DIRECTORY,backup_directory)
    
    # make a connection to the .sql file within the backup directory
    conn = sqlite3.connect(os.path.join(backup_directory, 'Manifest.db'))

    query = "SELECT * FROM File"
    try:
        output = conn.execute(query)
    except Exception as e:
        print(e)
    
parser = argparse.ArgumentParser()

parser.add_argument("-b", "--backup_directory", type=str, default=BACKUP_DIRECTORY)
parser.add_argument("-d", "--destination_directory", type=str, default=None)
parser.add_argument("-e", "--extensions", type=list)
args = vars(parser.parse_args())

extract_media(**args)