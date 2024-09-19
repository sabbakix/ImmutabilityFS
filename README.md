# ImmutabilityFS
Manage immutability attributes on Linux box for safeguarding your backup files

## Overview

ImmutabilityFS is a Python script designed to manage the immutability attributes of files on a Linux filesystem. It can check if a file is immutable, set a file to be immutable, and process specific types of backup files. At the moment, it set immutability for veeam backup files(.vbm,.vib,.vbk)

## Requirements

- Python 3.x
- Linux operating system
- `lsattr` and `chattr` commands available

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ImmutabilityFS.git
    cd ImmutabilityFS
    ```

2. Ensure you have the necessary permissions to run `lsattr` and `chattr` commands.

3. Customise the list of directories to keep immutable in the data.py file, and set the number of day to keep the file immutable.
    ```
        def imfolders():
        return {
            "/path/to/dir1":8,
            "/path/to/dir2":10
        }
    ```
4. Adding to Crontab. To schedule the script to run at regular intervals, you can add it to the crontab. For example, to run the script every day at midnight:
    1. Open the crontab editor:
    ```
        crontab -e
    ```
    2. Add the following line to schedule the script ever 2 hours:
    ```
        0 2 * * * /usr/bin/python3 /path/to/your/script/main.py
    ```

# License

This project is licensed under the MIT License. See the *LICENSE* file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.