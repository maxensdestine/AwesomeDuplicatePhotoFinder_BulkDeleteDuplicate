# Awesome Duplicate Photo Finder Bulk Delete Duplicate
Python CLI app to bulk delete duplicate images found with Awesome Duplicate Photo Finder

### Operating System
This app was only tested on WSL2 Ubuntu 20.04.1 LTS. It should theorically work for other Unix operating systems and for Windows 7+. Don't hesitate to provide feedback if it does not.

### Limits of This App
This app will not work if some of your files have a semicolon character ";" in their name. In Powershell, Windows users can change file names in bulk by using the command ```get-childitem * | foreach { rename-item $_ $_.Name.Replace(";", "_") }```. Unix users can achieve the same in their CLI with this command ```rename 's/;/_/g' *```. Please note that neither of these commands deals with the edge case where a file with that name already exists.

## Usage
Example for WSL2: ```python3 deldup.py -sim 50 /mnt/c/users/me/documents/output.csv```
CLI Argument | Short | Description |
--- | --- | --- | 
--similarity | -sim | Integer representing the minimum similarity percentage to delete a picture. Must be greater than 0. Default value: 80|
N/A (positional argument) | N/A | Path to the file which contains the Awesome duplicate photo finder output (semi colon separated values) |
