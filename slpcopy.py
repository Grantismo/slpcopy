import sys
from gooey import Gooey, GooeyParser
import dataclasses
import humanize
import pathlib
import psutil
import shutil
import io
import os
from colored import stylize, attr, fg

FAT32='FAT32'
SLP_EXTENSION='*.slp'


@dataclasses.dataclass
class Drive:
    name: str
    mountpoint: str
    size: int
    files: list

    def human_size(self):
        return humanize.naturalsize(self.size)


def get_devices():
    return [Drive(
        name=device.device,
        mountpoint=device.mountpoint,
        size=psutil.disk_usage(device.mountpoint).total
        ) for device in psutil.disk_partitions() if device.fstype==FAT32]

def find_slp_files(device):
    return list(pathlib.Path(device.mountpoint).rglob(SLP_EXTENSION))

def replay_folder_name(num):
    return "Setup {:03d}".format(num)

def resource_path(path):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, path)


@Gooey(program_name="SlpCopy",
       progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
       progress_expr="current / total * 100",
       richtext_controls=True,
       hide_progress_msg=True,
       image_dir=resource_path('img'),
       timing_options = {
         'show_time_remaining': True,
         'hide_time_remaining_on_complete': True,
       })
def main():
    parser = GooeyParser(description="blorppppp's *.slp copy tool. Copies all *.slp files from thumbdrives onto your machine.")
    parser.add_argument('output_path', metavar='Output Path', help='The directory to copy *.slp files into.', widget="DirChooser")
    # Value of the variable is the inverse of the selection in the checkbox.
    parser.add_argument('--keep_after_copy', metavar='Remove after copy', help='Delete original *.slp files off thumbdrives after succesfully copying to your machine.', action="store_false")
    
    args = parser.parse_args()

    devices = get_devices()
    if devices: 
        print(stylize('Searching {} connected devices for *.slp files.'.format(len(devices)), attr('bold')))
    else:
        print(stylize('No conncted devices to search.', fg('dark_gray') + attr('bold')))

    output_path = pathlib.Path(args.output_path)

    cur_dir = 0
    for device in devices:
        print(stylize('Searching device {} ({})'.format(device.name, device.human_size()), fg('light_blue')))
        slp_files = find_slp_files(device)
        if slp_files:
            print(stylize('Found {} slp replay files.'.format(len(slp_files)), fg('light_blue') + attr('bold')))
            device.files = slp_files
        else:
            print(stylize('Found no slp replay files.', fg('light_gray')))
        print()

    total_files = sum(len(d.files) for d in devices)
    i = 0
    if not total_files: 
        print(stylize('No files to copy.', fg('dark_gray') + attr('bold')))
    for device in devices:
        if not device.files:
            continue
        while True:
            folder_name = pathlib.Path(output_path).joinpath(replay_folder_name(cur_dir))
            if not folder_name.exists():
                folder_name.mkdir(parents=True, exist_ok=False)
                break
            cur_dir += 1
        for f in device.files:
            print(f)
            print("progress: {}/{}".format(i + 1, total_files))
            sys.stdout.flush()
            shutil.copy(f, folder_name)
            if not args.keep_after_copy:
                f.unlink()
            i += 1
        print(stylize('Copied {} slp replay files from to {}'.format(len(device.files), device.name, folder_name.resolve()), fg('green')))
        if not args.keep_after_copy:
            print(stylize('Deleted {} replay files from {}'.format(len(device.files), device.name), fg('green')))
    print(stylize('Complete.', fg('green') + attr('bold')))


if __name__ == '__main__':
    main()
