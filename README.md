# slpcopy
Tool to copy all *.slp files (from [Slippi](https://github.com/project-slippi/project-slippi) tournament captures) from attached thumbdrives. Useful for TOs running a SSBM tournament. 

![Screenshot](https://imgur.com/6boYxzE.png)

## Features

* Scans all attached FAT32 formatted drives.
* Copies all *.slp replay files into a directory of your choice on your machine.
* Organizes *.slp replay files by thumbdrive in the output directory.
* Optionally deletes *.slp replay files after copying. 
* Optionally uses custom drive names in output directory.
* **[New!] Optionally renames files on copy to a more human readable format (e.g. "Game_20211025T160457.slp" --> "20211025T160457 - Fox (Green) vs Samus (Green) - Battlefield.slp")**
* Full Windows & Linux support. OSX should also work if you run the python script directly, but this is untested.
* 
<img src="https://i.imgur.com/zAGVtME.png" width="200">
<img src="https://i.imgur.com/VZsv6hr.png" width="600">


## Installation

* Grab the latest release from https://github.com/Grantismo/slpcopy/releases
* Unzip and run slpcopy.exe
![Screenshot](https://i.imgur.com/2kktTeK.png)

## Usage
1. Plug in all thumbdrives you'd like to pull *.slp files off. 
1. Choose a directory to copy files into.
1. Choose settings: (Optionally delete originals after copy and/or use custom drive names).
1. Hit 'Start'.

Works well with a multiport usb hub:

<img src="https://i.imgur.com/tDVmnau.jpg" width="300">

## CLI Usage

```
$ python slpcopy.py --ignore-gooey --help
usage: slpcopy.py [-h] [--remove_after_copy] [--use_custom_drive_names] [--rename_files] Output Path

blorppppp's *.slp copy tool. Copies all *.slp files from thumbdrives onto your machine.

positional arguments:
  Output Path           The directory to copy *.slp files into.

options:
  -h, --help            show this help message and exit
  --remove_after_copy   Delete original *.slp files off thumbdrives after succesfully copying to your machine.
  --use_custom_drive_names
                        Copy *.slp files into a folder with each thumbdrive's custom name (if applicable). If unchecked a new folder will be created for each drive (e.g. "Setup 001")
  --rename_files        Rename *.slp files into a more human readable format. "Game_20211025T160457.slp" -> "20211025T160457 - Fox (Green) vs Samus (Green) - Battlefield.slp"
```
<img src="https://imgur.com/ornd613.jpg" width="900">

## Tips
### How to set up Slippi replay recording on your Wii
https://www.youtube.com/watch?v=KiJZX-GUyak&ab_channel=YashichiSSBM

### Prevent File Explorer popup when you plug in a thumbdrive
https://www.windowscentral.com/how-configure-autoplay-windows-10
