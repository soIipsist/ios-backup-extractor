# iOS backup extractor

A simple Python script for extracting media files from an iOS backup directory.

This script retrieves all media files from an iOS backup, and transfers them to a specified destination directory.

## Arguments

The following command-line arguments can be used to customize the behavior of the script:

- **`-b` / `--backup_directory`**  
  **Type**: `str`  
  **Default**: The most recently created backup directory (located by default in `~/Library/Application Support/MobileSync/Backup/`).
  **Description**: Specifies the path to the iOS backup directory. If not provided, the default backup directory will be used.

- **`-o` / `--output_directory`**  
  **Type**: `str`  
  **Default**: `desktop_path`  
  **Description**: Defines the destination directory for the extracted media files. By default, files will be moved to the Desktop.

- **`-d` / `--domains`**  
  **Type**: `list`  
  **Default**: `[Domain.FILES]`  
  **Description**: Filters the backup by specified domains (categories of files). Defaults to processing `Domain.FILES` if not provided.

- **`-e` / `--extensions`**  
  **Type**: `list` of `str` (optional)  
  **Default**: `None`  
  **Description**: Filters files by specified extensions (e.g., `mp4`, `jpg`). If omitted, all file types will be processed.

- **`-r` / `--remove_backup`**  
  **Type**: `bool`  
  **Default**: `False`  
  **Description**: If `True`, the script will remove the original backup files after processing them.
  
## Usage Example

```bash
python extract.py -b /path/to/backup_directory -o /path/to/output_directory -d files photos -e mp4 jpg -r True
```

- **`-b`**: Path to the iOS backup directory.
- **`-o`**: Destination directory for extracted media files.
- **`-d`**: Specifies the domains (e.g., `Domain.FILES`, `Domain.PHOTOS`).
- **`-e`**: File extensions to include (e.g., `mp4`, `jpg`).
- **`-r`**: If `True`, removes the backup files after extraction.
